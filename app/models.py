# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UnicodeText, Date
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
    dob = db.Column(Date)
    repository = db.Column(db.String(120))
    social_red = db.Column(db.String(150))
    create_date_personal = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, name, last_name, sex, country, dob, repository, social_red):
        self.id_user = id_user
        self.name = name
        self.last_name = last_name
        self.sex = sex
        self.country = country
        self.dob = dob
        self.repository = repository
        self.social_red = social_red


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
    """"Many to Many..."""
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_name = db.Column(db.String(30))


class Question(db.Model):
    __tablename__ = 'user_question'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    text_area = db.Column(UnicodeText)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, title, description, text_area):
        self.id_user = id_user
        self.title = title
        self.description = description
        self.text_area = text_area


class TagQuestion(db.Model):
    __tablename__ = 'tag_question'
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'), nullable=False)
    tag_relation = db.relationship('Question', backref=db.backref('user_question_tag',
                                               cascade="all, delete-orphan"), lazy='joined')
    tag_one = db.Column(db.String(25),  nullable=True)
    tag_two = db.Column(db.String(25),  nullable=True)
    tag_three = db.Column(db.String(25), nullable=True)

    def __init__(self, id_question, tag_one, tag_two, tag_three):
        self.id_question = id_question
        self.tag_one = tag_one
        self.tag_two = tag_two
        self.tag_three = tag_three


class AnswerLong(db.Model):
    __tablename__ = 'user_answer_long'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'))
    question = db.relationship('Question', backref=db.backref('user_question_answer',
                                           cascade="all, delete-orphan"), lazy='joined')
    name_user = db.Column(db.String(80), nullable=False)
    answer = db.Column(db.String(2000), nullable=False)
    answer_code = db.Column(UnicodeText, nullable=True)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, name_user, id_question, answer, answer_code):
        self.id_user = id_user
        self.name_user = name_user
        self.id_question = id_question
        self.answer = answer
        self.answer_code = answer_code


class Snippet(db.Model):
    __tablename__ = 'user_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(45))
    description = db.Column(db.String(250))
    text_area = db.Column(UnicodeText)
    star = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, title, description, text_area):
        self.id_user = id_user
        self.title = title
        self.description = description
        self.text_area = text_area


class TagSnippet(db.Model):
    __tablename__ = 'tag_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_snippet = db.Column(db.Integer, db.ForeignKey('user_snippet.id'), nullable=False)
    tag_relation = db.relationship('Snippet', backref=db.backref('user_snippet_tag',
                                              cascade="all, delete-orphan"), lazy='joined')
    tag_one = db.Column(db.String(25),  nullable=True)
    tag_two = db.Column(db.String(25),  nullable=True)
    tag_three = db.Column(db.String(25), nullable=True)

    def __init__(self, id_snippet, tag_one, tag_two, tag_three):
        self.id_snippet = id_snippet
        self.tag_one = tag_one
        self.tag_two = tag_two
        self.tag_three = tag_three


class CommentSnippet(db.Model):
    __tablename__ = 'comment_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_snippet = db.Column(db.Integer, db.ForeignKey('user_snippet.id'), nullable=False)
    tag_relation = db.relationship('Snippet', backref=db.backref('user_snippet_comment',
                                              cascade="all, delete-orphan"), lazy='joined')
    commet_user = db.Column(db.String(80), nullable=False)
    comment_text = db.Column(db.String(120), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, id_snippet, commet_user, comment_text):
        self.id_user = id_user
        self.id_snippet = id_snippet
        self.commet_user = commet_user
        self.comment_text = comment_text
