from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import render_template
from flask_sqlalchemy import SQLAlchemy, event

from main import app

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)

    label = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Integer(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def on_add(*args):
        print(args)
        emit("api:update_index", {"status": 1, "items": [{"action": 1,"post": render_template("post_template.html", post=args[2])}]}, to="index")

    def on_delete(*args):
        print(args)
        emit("api:update_index", {"status": 1, "items": [{"action": 0,"post": args[2].id}]}, to="index")
    
    def on_edit(*args):
        print(args)
        emit("api:update_index", {"status": 1, "items": [{"action": 2,"post": render_template("post_template.html", post=args[2])}]}, to="index")
