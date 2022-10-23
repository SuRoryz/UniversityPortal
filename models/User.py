from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template
from flask_sqlalchemy import SQLAlchemy, event

from main import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    active = db.Column(db.Boolean()),
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    role = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='custom_user', lazy=True)
    files = db.relationship('File', backref='custom_user', lazy=True)
    mail_by = db.relationship('Mail', backref='sender', lazy='dynamic', foreign_keys = 'Mail.idsender')
    mail_to = db.relationship('Mail', backref='reciever', lazy='dynamic', foreign_keys = 'Mail.idreciever')

    is_prof = db.Column(db.Boolean(), default=False)
    group = db.Column(db.String(50), nullable=True)

    room = db.Column(db.String(50), nullable=False)

    resfresh_token = db.Column(db.String(255), nullable=True)
    
    def match_password(self, password):
        if password == self.password:
            return True
        return False
    
    def on_add(*args):
        pass

    def on_delete(*args):
        pass
    
    def on_edit(*args):
        pass