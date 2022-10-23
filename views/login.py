from main import app
from flask import request, Response, render_template

from forms.LoginForm import LoginForm

@app.route('/login')
def login_page():
    form = LoginForm()
    return Response(response=render_template('login.html', form=form), status=200)
