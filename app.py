from json import loads, dumps

from flask_socketio import SocketIO
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy, event
from flask_user import UserManager

from models.User import User
from models.Mail import Mail
from models.File import File
from models.Post import Post

from utils import date_converter, get_user_by_id

SUPERMEGASECRET = "DJASDNJasJHDASHJIFH2j4h3J$HJ@NCHJKW" # Secret
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 30
REF_EXP_DELTA_SECONDS = 9900

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////new11.db?autocommit=true'
app.config['USER_EMAIL_SENDER_EMAIL'] = 'test@test.com'
app.config['SECRET_KEY'] = SUPERMEGASECRET
app.config['UPLOAD_FOLDER'] = "upload/"
app.config['UPLOAD_FOLDER_SHLEUDE'] = "upload/shleude/"

socketio = SocketIO(app)

db = SQLAlchemy(app)

for model in [User, Mail, File, Post]:
    event.listen(model, 'after_insert', model.on_add)
    event.listen(model, 'after_delete', model.on_delete)
    event.listen(model, 'after_update', model.on_edit)

def get_user():
    return request.user.id

user_manager = UserManager(app, db, User)
db.create_all()

app.jinja_env.globals.update(date_converter=date_converter, get_user_by_id=get_user_by_id)

socketio.run(app, debug=True)
