import cryptocode
import time

from json import loads

from flask_sqlalchemy import SQLAlchemy, event
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request, Response, render_template, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

from forms.RegistrationForm import RegistrationForm
from forms.LoginForm import LoginForm
from api.api_utils import socket_wrapper
from models.User import User
from models.Mail import Mail
from models.File import File
from models.Post import Post
from main import app, socketio, create_access_token, get_user, REF_EXP_DELTA_SECONDS, SUPERMEGASECRET

from encryption import auth_middleware

from utils import encrypt_room, decrypt_room
from api.api_utils import admin_tabs, admin_windows, admin_removes, admin_adds

from xls_parser import Parser

db = SQLAlchemy(app)

@app.route('/api/resfresh_token')
@auth_middleware()
def refresh_token():
    user = get_user()
    jwt_token = create_access_token(user)

@app.route('/api/upload', methods=["POST"])
@auth_middleware()
def upload():
    action = request.form["action"]

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)

        if action == "shleude":
            path = app.config["UPLOAD_FOLDER_SHLEUDE"] + "rasp.xls"
        else:
            path = app.config["UPLOAD_FOLDERE"] + filename

        file.save(path)
        obj = File(path=path, name=filename, date=int(time.time()))
        db.session.add(obj)
        db.session.commit()
        
    return Response(status=200)

@socketio.on('api:message_new')
@auth_middleware(API=True)
@socket_wrapper(event='api:message_new')
def on_message_new(data):
    rek = User.query.filter_by(role="Ректор").first()

    if rek.id == request.user.id:
        print()
        reciever = User.query.filter_by(id=int(loads(data)["to"])).first()
        to_rek = False
    else:
        reciever = rek
        to_rek = True

    msg = Mail(text=loads(data)["text"], date=int(time.time()), idsender=request.user.id, idreciever=reciever.id, to_rek=to_rek)

    db.session.add(msg)
    db.session.commit()

@socketio.on('api:register')
def register(data):

    form = RegistrationForm(ImmutableMultiDict(loads(data)["data"]))
    user = User.query.filter_by(email=form.email.data).first()

    if user:
        emit("api:register", {"status": 0, "items": ["Пользователь уже существует"]})
        return
    
    if form.validate():
        room = cryptocode.encrypt(form.email.data, SUPERMEGASECRET)

        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data, first_name=form.firstname.data, last_name=form.lastname.data, role=form.role.data ,room=room,
                    is_prof=form.is_prof.data, group=form.group.data)
                
        db.session.add(user)
        db.session.commit()
        emit("api:register", {"status": 1, "items": [{"next": "login"}]})
        return

    emit("api:register", {"status": 0, "items": [form.errors]})
    


@socketio.on('api:login')
def login(data):

    form = LoginForm(ImmutableMultiDict(loads(data)["data"]))
    user = User.query.filter_by(email=form.email.data).first()

    if form.validate():
        try:
            if not(user.match_password(form.password.data)) or not(user):
                emit("api:login", {"status": 0, "items": ["Такого пользователя не существует"]})
        except:
            emit("api:login", {"status": 0, "items": ["Такого пользователя не существует"]})

        jwt_token = create_access_token(user)
        refresh = create_access_token(user, True, jwt_token)

        expire_date = int(time.time()) + REF_EXP_DELTA_SECONDS

        emit("api:login", {"status": 1, "items": [{"token": cryptocode.encrypt(jwt_token, SUPERMEGASECRET), "ref_token": cryptocode.encrypt(refresh, SUPERMEGASECRET), "ref_token_exp": expire_date, "next": "index"}]})

        return
    
    emit("api:login", {"status": 0, "items": ["Такого пользователя не существует"]})


@socketio.on('api:join')
@auth_middleware(API=True)
@socket_wrapper(event='api:join')
def on_join(data):
    room = loads(data)['room']
    if "private" in loads(data).keys():
        room = decrypt_room(room)

    join_room(room)
    emit("api:hooked", {"status": 1}, to=room)

    if "private" in loads(data).keys():
        mails = Mail.query.filter_by(idsender=request.user.id).limit(10)
        emit("api:message_history", {"status": 1, "items": [render_template("message_history.html", mails=mails)]}, to=room)

@socketio.on('api:leave')
@auth_middleware(API=True)
@socket_wrapper(event='api:leave')
def on_leave(data):
    room = loads(data)['room']
    leave_room(room)
    emit("api:unhooked", {"status": 1}, to=room)

@socketio.on('api:draw_shleude')
@auth_middleware(API=True)
@socket_wrapper(event='api:draw_shleude')
def draw_rasp(data):
    group = int(loads(data)["group_id"])
    shleude = Parser.parse_xls("rasp.xls")

    print(shleude)

    emit("api:draw_shleude", {"status": 1, "items": [render_template("shleude_template.html", json=shleude[list(shleude.keys())[group]])]})

@socketio.on('api:admin_get_tab')
@auth_middleware(API=True)
@socket_wrapper(event='api:admin_get_tab')
def get_tab(data):
    action = loads(data)["action"]
    emit("api:admin_get_tab", {"status": 1, "items": [admin_tabs[action](request)]})


@socketio.on('api:admin_open_rektor_dialog')
@auth_middleware(API=True)
@socket_wrapper(event='api:admin_open_rektor_dialog')
def get_tab(data):
    user_id = loads(data)["user_id"]

    room = encrypt_room(User.query.filter_by(id=user_id).first().email)

    messages = Mail.query.filter_by(idsender=user_id).all()
    emit("api:admin_open_rektor_dialog", {"status": 1, "items": [render_template("admin_tabs/admin_rektor_dialog.html", mails=messages, tkn=room, user_id=messages[0].idsender)]})

@socketio.on('api:admin_get_add_window')
@auth_middleware(API=True)
@socket_wrapper(event='api:admin_get_add_window')
def get_add_window(data):
    action = loads(data)["action"]
    emit("api:admin_get_add_window", {"status": 1, "items": [admin_windows[action](request)]})

@socketio.on('api:admin_add')
@auth_middleware(API=True)
@socket_wrapper(event='api:admin_add')
def add(data):
    data = loads(data)

    action = data["action"]
    form = data["formData"]

    obj = admin_adds[action](form)
    db.session.add(obj)
    db.session.commit()
    
    emit("api:admin_get_tab", {"status": 1, "items": [admin_tabs[action](request)]})

@socketio.on('api:admin_remove')
@auth_middleware(API=True)
@socket_wrapper(event='api:admin_remove')
def remove(data):
    data = loads(data)

    action = data["action"].split("-")[0]
    delete_id = data["action"].split("-")[1]

    admin_removes[action](delete_id)
    db.session.commit()
    
    emit("api:admin_get_tab", {"status": 1, "items": [admin_tabs[action](request)]})
