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
    skill = db.relationship('Skills', backref='user', lazy='dynamic')
    question = db.relationship('Question', backref='user', lazy='dynamic')
    answer_longer = db.relationship('AnswerLong', backref='user', lazy='dynamic')

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


    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Curriculum_User(db.Model):
    __tablename__ = 'user_curriculum_info'
    id_curriculum = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    tittle = db.Column(db.String(100))
    university = db.Column(db.String(200))
    description = db.Column(db.String(260))
    create_date_curriculum = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, tittle, university, description):
        self.id_user = id_user
        self.tittle = tittle
        self.university = university
        self.description = description


class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_name = db.Column(db.String(30))

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Question(db.Model):
    __tablename__ = 'user_question'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    text_area = db.Column(UnicodeText)
    answer_long = db.relationship('AnswerLong', backref='user_question', lazy='dynamic')
    tag_relation = db.relationship('TagQuestion', backref='user_question', lazy='dynamic')
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, title, description, text_area):
        self.id_user = id_user
        self.title = title
        self.description = description
        self.text_area = text_area

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

class TagQuestion(db.Model):
    __tablename__ = 'tag_question'
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'))
    tag_one = db.Column(db.String(25),  nullable=True)
    tag_two = db.Column(db.String(25),  nullable=True)
    tag_three = db.Column(db.String(25), nullable=True)

    def __init__(self, id_question, tag_one, tag_two, tag_three):
        self.id_question = id_question
        self.tag_one = tag_one
        self.tag_two = tag_two
        self.tag_three = tag_three

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class AnswerLong(db.Model):
    __tablename__ = 'user_answer_long'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'))
    answer = db.Column(db.String(2000))
    answer_code = db.Column(UnicodeText)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, id_question, answer, answer_code):
        self.id_user = id_user
        self.id_question = id_question
        self.answer = answer
        self.answer_code = answer_code

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
