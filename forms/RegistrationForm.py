from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField, PasswordField, validators)
from wtforms.validators import InputRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Псевдоним', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Почта', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Повторите пароль')
    firstname = StringField('Имя', [validators.Length(min=2, max=30), validators.DataRequired()])
    lastname = StringField('Фамилия', [validators.Length(min=2, max=30), validators.DataRequired()])
    role = StringField('Должность', [validators.Length(min=2, max=30), validators.DataRequired()])
    is_prof = BooleanField('В профсоюзе')
    group = StringField('Группа', [validators.Length(min=2, max=30), validators.Optional()])