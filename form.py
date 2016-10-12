# coding=utf-8
from wtforms import Form, StringField, validators, PasswordField, SelectField, DateTimeField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
import pycountry

class Country_dict(dict):
    cc = {}
    t = list(pycountry.countries)

    for country in t:
        cc[country.alpha2] = country.name

countries = Country_dict()


class RegisterForm(Form):
    username = StringField('',   [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=5, message='Min 5 letter, Try Again')])
    password = PasswordField('', [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=8, message='Min 8 letter, Try Again')])
    email = EmailField('',       [validators.Email('Ingrese un email valido'), validators.DataRequired(message='El campo esta vacio.'), validators.length(min=7, message='Min:5, letter, Try Again')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

class LoginForm(Form):
    username = StringField('',   [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=5, message='Min 5 letter, Try Again')])
    password = PasswordField('', [validators.DataRequired(message='El campo esta vacio.'), validators.length(min=8, message='Min 8 letter, Try Again')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

class PersonalForm(Form):
    name = StringField('First Name..',   [validators.DataRequired(message='El campo esta vacio.')])
    last_name = StringField('Last Name..',   [validators.DataRequired(message='El campo esta vacio.')])
    sex = SelectField('Select your sex', choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Transgendered')])
    country = SelectField('Country', choices=[('VE', 'Venezuela'), ('AS', 'Australia'), ('NY', 'New York')])
    city = StringField('City',   [validators.DataRequired(message='El campo esta vacio.')])
    dob = DateField('DOB')
    repository = StringField('Repository', [validators.DataRequired(message='El campo esta vacio.')])
    social_red = StringField('Social', [validators.DataRequired(message='El campo esta vacio.')])


class CurriculumForm(Form):
    tittle = StringField('Your tittle or Job',   [validators.DataRequired(message='El campo esta vacio.')])
    first_skill = StringField('First skill',   [validators.DataRequired(message='El campo esta vacio.')])
    second_skill = StringField('Second skill',   [validators.DataRequired(message='El campo esta vacio.')])
    other_skill = StringField('Other skill',   [validators.DataRequired(message='El campo esta vacio.')])
    university = StringField('Univeruty or Alma mater',   [validators.DataRequired(message='El campo esta vacio.')])
    years = IntegerField('Years',   [validators.DataRequired(message='El campo esta vacio.')])
    description = StringField('Your description',   [validators.DataRequired(message='El campo esta vacio.')])