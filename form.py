# coding=utf-8
from wtforms import Form, StringField, validators, PasswordField, SelectField, DateTimeField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
import pycountry

class Country_list(list):
    """'create choice for html form"""
    def __init__(self):
        self.lista_alpha = []
        self.lista_name = []
        self.choice = None

    def create_choices(self):
        t = list(pycountry.countries)
        for country in t:
            self.lista_alpha.append(country.alpha2)
            self.lista_name.append(country.name)
        self.choice = zip(self.lista_alpha, self.lista_name)
        return self.choice

countries = Country_list()
choices_class = countries.create_choices()

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
    country = SelectField('Country', choices=choices_class)
    city = StringField('City',   [validators.DataRequired(message='El campo esta vacio.')])
    dob = DateField('DOB', format="%m/%d/%Y")
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
