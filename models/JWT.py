from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template
from flask_sqlalchemy import SQLAlchemy, event

from main import app

db = SQLAlchemy(app)

class JWT(db.Model):
    __tablename__ = 'keys'

    kid = db.Column(db.String(255), nullable=False, primary_key=True)
    secret = db.Column(db.String(255), nullable=False)
    jwt = db.Column(db.String(255), nullable=True)