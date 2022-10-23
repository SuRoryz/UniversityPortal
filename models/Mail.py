from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template
from flask_sqlalchemy import SQLAlchemy, event

from models.User import User

from main import app

db = SQLAlchemy(app)

class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Integer(), nullable=False)

    idreciever = db.Column(db.Integer, db.ForeignKey('users.id'))
    idsender = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_rek = db.Column(db.Boolean, default=False)

    answered = db.Column(db.Boolean, default=False)

    def on_add(*args):
        if args[2].to_rek:
            room = User.query.filter_by(id=args[2].idsender).first().email
        else:
            room = User.query.filter_by(id=args[2].idreciever).first().email
            #Mail.query.filter_by(idsender=args[2].idreciever).update({Mail.answered: True})
            #db.session.commit()
        
        print('What', room)
        emit("api:message_new", {"status": 1, "items": [render_template("message.html", message=args[2])]}, to=room)

    def on_delete(*args):
        pass
    
    def on_edit(*args):
        pass