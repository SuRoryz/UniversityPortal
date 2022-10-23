
from main import app
from encryption import auth_middleware

from flask import request, Response, redirect, render_template

from models.User import User


@app.route('/profile')
@auth_middleware()
def profile():
    return redirect(f"profile/{request.user.username}")

@app.route('/profile/<name>')
@auth_middleware()
def profile_named(name):
    return Response(response=render_template('profile.html', user=User.query.filter_by(username=name).first()), status=200)
