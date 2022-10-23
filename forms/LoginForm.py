from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField, PasswordField, validators)
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Почта', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
    ])