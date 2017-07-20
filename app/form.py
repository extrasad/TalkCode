# coding=utf-8
from wtforms import *
from flask_security import current_user
from flask_security.forms import RegisterForm
from wtforms.widgets import TextArea
from app import db, User, Personal_User, Curriculum_User, Question

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


class SecurityRegisterForm(RegisterForm):
    username = StringField('Username',   [
        validators.Regexp('^\w+$', message="Regex: Username must contain only letters numbers or underscore"),
        validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=5, message='Min 5 letter, Try Again')])

    def validate(self):
        #Check for username because is unique
        if db.session.query(User).filter(User.username == self.username.data.strip()).first():
            self.username.errors = list(self.username.errors)
            self.username.errors.append('The username already use')
            return False

        #Now check for Flask-Security validate functions
        if not super(SecurityRegisterForm, self).validate():
            return False

        return True


class PersonalForm(Form):

    first_name = StringField('First Name..', [validators.Regexp('^[A-z]+$',
        message="Regex: Username must contain only letters"),
        validators.DataRequired(message='El campo esta vacio.')])

    last_name = StringField('Last Name..',   [validators.Regexp('^[A-z]+$',
        message="Regex: Username must contain only letters"),
        validators.DataRequired(message='El campo esta vacio.')])

    repository = StringField('Repository',   [validators.URL(require_tld=True,
        message=u'Invalid URL.'), validators.DataRequired(message='El campo esta vacio.')])

    social_red = StringField('Social',       [validators.URL(require_tld=True,
        message=u'Invalid URL.'), validators.DataRequired(message='El campo esta vacio.')])

    sex = SelectField('Select your sex', choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Transgendered')])

    country = SelectField('Country', choices=choices_class)

    dob  = DateField('DOB')

    def validate(self, model):
        if not super(PersonalForm, self).validate():
            return False

        if model is None:
            model = Personal_User(id_user=current_user.id, first_name=self.first_name.data,
                                  last_name=self.last_name.data, sex=self.sex.data,
                                  country=self.country.data, dob=self.dob.data,
                                  repository=self.repository.data, social_red=self.social_red)
        else:
            model.last_name = self.last_name.data
            model.first_name = self.first_name.data
            model.country = self.country.data
            model.sex = self.sex.data
            model.country = self.country.data
            model.repository = self.repository.data
            model.social_red = self.social_red.data

        db.session.add(model)
        db.session.commit()

        return True


class CurriculumForm(Form):

    tittle = StringField('Your tittle or Job',
        [validators.DataRequired(message='El campo esta vacio.')])

    university = StringField('University o College',
        [validators.DataRequired(message='El campo esta vacio.')])

    description = StringField('Your description',
        [validators.DataRequired(message='El campo esta vacio.')])

    def validate(self, model):
        if not super(CurriculumForm, self).validate():
            return False

        if model is None:
            model = Curriculum_User(id_user=current_user.id,
                                    tittle=self.tittle.data,
                                    university=self.university.data,
                                    description=self.description.data)
        else:
            model.tittle = self.tittle.data
            model.university = self.university.data
            model.description = self.description.data

        db.session.add(model)
        db.session.commit()

        return True



class QuestionForm(Form):

    tittle = StringField('',     [validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=5, max=350, message='Min 5, Max 350')])

    description = StringField('',[validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=15, max=1000, message='Min 15, Max 1000')],
        render_kw={"placeholder": "", "rows": 3}, widget=TextArea())

    text_area = StringField('',  [validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=50, max=2500, message='Min 50, Max 2000')],
        render_kw={"placeholder": "Code . . ."}, widget=TextArea())

    tag_one = StringField('',     [validators.length(min=2, max=25, message='Max 25')],
        render_kw={"placeholder": "#C++"})

    tag_two = StringField('',     [validators.length(min=2, max=25, message='Max 25')],
        render_kw={"placeholder": "#Python"})

    tag_three = StringField('',   [validators.length(min=2, max=25, message='Max 25')],
        render_kw={"placeholder": "#Databases"})


class AnswerForm(Form):

    answer_long = StringField('',    [validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=20, max=250, message='Min 20, Max 250')],
        render_kw={"placeholder": "Answer . . .",}, widget=TextArea())

    text_area = StringField('',      [validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=8, max=2000, message='Min 8, Max 2000')],
        render_kw={"placeholder": "Code . . ."}, widget=TextArea())


class SnippetsForm(Form):

    tittle = StringField('',      [validators.Regexp(r'^[\w,\s-]+\.[A-Za-z]{1,5}$',
        message="Regex: Snippet need file extension"),
        validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=5, max=45, message='Min 5, Max 45')])

    description = StringField('',[validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=15, max=250, message='Min 15, Max 50')])

    text_area = StringField('',  [validators.DataRequired(message='El campo esta vacio.'),
        validators.length(min=5, message='Min 5')], widget=TextArea())

    tag_one = StringField('',    [validators.length(min=1, max=25, message='Max 25')],
        render_kw={"placeholder": "#Algorithm"})

    tag_two = StringField('',    [validators.length(min=1, max=25, message='Max 25')],
        render_kw={"placeholder": "#Class"})

    tag_three = StringField('',  [validators.length(min=1, max=25, message='Max 25')],
        render_kw={"placeholder": "#Data Structure"})


class SnippetsComment(Form):

    comment = StringField('', [validators.DataRequired(message='El campo esta vacio.'),
                               validators.length(min=5, max=120, message='Min 5, Max 120')])


class SkillForm(Form):

    skill_name = StringField('Skill name',
                             [validators.DataRequired(message='El campo esta vacio.')])