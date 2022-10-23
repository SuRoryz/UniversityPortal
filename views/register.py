from main import app
from encryption import auth_middleware

from flask import request, Response, render_template

from forms.RegistrationForm import RegistrationForm

@app.route('/register')
def register_page():
    form = RegistrationForm()
    return Response(response=render_template('register.html', form=form), status=200)
