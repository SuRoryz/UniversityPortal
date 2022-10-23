import time

from flask import request, Response, render_template
from flask_sqlalchemy import SQLAlchemy, event
from flask_socketio import emit

from models.Post import Post
from models.User import User
from models.File import File
from models.Mail import Mail

from main import app

db = SQLAlchemy(app)

def socket_wrapper(event):
    def wraps(f):
        def wraps_(*args, **kwargs):
            if hasattr(request, "stat"):
                emit(event, {"status": 0, "items": []})
            else:
                try:
                    f(*args, **kwargs)
                except Exception as e:
                    print(e)
                    emit(event, {"status": 2, "items": [str(e)]})
                    
        return wraps_
    return wraps

admin_tabs = {
    "users": lambda request: render_template(f"admin_tabs/admin_users.html", users = User.query.all()),
    "news": lambda request: render_template(f"admin_tabs/admin_news.html", posts = Post.query.all()),
    "rasp": lambda request: render_template(f"admin_tabs/admin_rasp.html", files = File.query.all()),
    "rektor": lambda request: render_template(f"admin_tabs/admin_rektor.html", mails = Mail.query.filter(Mail.answered == False, Mail.to_rek == True).all()),
    }

admin_windows = {
        "add-user": lambda request: render_template(f"admin_windows/admin_users.html", users = User.query.all()),
        "add-news": lambda request: render_template(f"admin_windows/admin_news.html", posts = Post.query.all()),
        "add-rasp": lambda request: render_template(f"admin_windows/admin_rasp.html", rasp = ""),
        "add-rektor": lambda request: render_template(f"admin_windows/admin_rektor.html", rektor = ""),
    }

admin_removes = {
        "users": lambda id: db.session.delete(User.query.filter_by(id=id).first()),
        "news": lambda id: db.session.delete(Post.query.filter_by(id=id).first()),
        "rasp": lambda id: db.session.delete(File.query.filter_by(id=id).first()),
        "rektor": lambda id: db.session.delete(Mail.query.filter_by(id=id).first()),
    }

admin_adds = {
        "users": create_user,
        "news": lambda data: Post(label=data["label"], text=data["text"], user_id=int(data["user_id"]),
                                  date=int(time.time())),
    }
