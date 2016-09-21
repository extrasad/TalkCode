# coding=utf-8
from wtforms import Form, StringField, validators, PasswordField
from wtforms.fields.html5 import EmailField

class GeneralForm(Form):
    username = StringField('',   [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=5, message='Min 5 letter, Try Again')])
    password = PasswordField('', [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=8, message='Min 8 letter, Try Again')])
    email = EmailField('',       [validators.Email('Ingrese un email valido'), validators.DataRequired(message='El campo esta vacio.'), validators.length(min=7, message='Min:5, letter, Try Again')])
    comment = StringField('',    [validators.DataRequired(message='El campo esta vacio'), validators.length(max=120, min=20, message='Min 20 letter, Try Again')])
    skill = StringField('Your skill in programming', [validators.DataRequired(message='El campo esta vacio')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
