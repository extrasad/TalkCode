# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UnicodeText
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(66))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    curriculum_date = db.relationship('Curriculum_User')
    personal_date = db.relationship('Personal_User')
    question = db.relationship('Question', backref='user', lazy='dynamic')
    answer = db.relationship('Answer', backref='user', lazy='dynamic')


    def __init__(self, username, password, email):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return "<User(id='%s',name='%s', email='%s', password='%s')>" % \
               (self.id, self.username, self.email, self.password)

class Personal_User(db.Model):
    __tablename__ = 'user_personal_info'
    id_personal_user = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    country = db.Column(db.String(45))
    city = db.Column(db.String(45))
    dob = db.Column(db.Date)
    repository = db.Column(db.String(120))
    social_red = db.Column(db.String(150))
    create_date_personal = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, name, last_name, sex, country, city, dob, repository, social_red):
        self.id_user = id_user
        self.name = name
        self.last_name = last_name
        self.sex = sex
        self.country = country
        self.city = city
        self.dob = dob
        self.repository = repository
        self.social_red = social_red


class Curriculum_User(db.Model):
    __tablename__ = 'user_curriculum_info'
    id_curriculum = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    tittle = db.Column(db.String(100))
    first_skill = db.Column(db.String(100))
    second_skill = db.Column(db.String(100))
    other_skill = db.Column(db.String(100))
    university = db.Column(db.String(200))
    years = db.Column(db.SmallInteger)
    description = db.Column(db.String(260))
    create_date_curriculum = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, tittle, first_skill, second_skill, other_skill, university, years, description):
        self.tittle = tittle
        self.first_skill = first_skill
        self.second_skill = second_skill
        self.other_skill = other_skill
        self.university = university
        self.years = years
        self.description = description


class Question(db.Model):
    __tablename__ = 'user_question'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    description = db.Column(db.String(200))
    text_area = db.Column(UnicodeText)
    tag = db.Column(db.String(45))
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Answer(db.Model):
    __tablename__ = 'user_answer'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.Column(UnicodeText)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
