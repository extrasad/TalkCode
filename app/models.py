# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UnicodeText, Date, Table, func
from flask_security import RoleMixin
from sqlalchemy_utils import aggregated
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        try:
            return unicode(self.name)  # python 2
        except NameError:
            return str(self.name)  # python 3

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(66))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    skills = db.relationship('Skill')
    curriculum_date = db.relationship('Curriculum_User')
    personal_date = db.relationship('Personal_User')
    question = db.relationship('Question', backref='userquestion', lazy='dynamic')
    answer_longer = db.relationship('AnswerLong', backref='useranswer', lazy='dynamic')
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
            

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email

    def __repr__(self):
        return "<User(id='%s',name='%s', email='%s', password='%s')>" % \
               (self.id, self.username, self.email, self.password)

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_question(self):
        return Question.query.join(followers, (followers.c.followed_id == Question.id_user)).filter(
            followers.c.follower_id == self.id).order_by(Question.create_date.desc())

    def followed_answer(self):
        return AnswerLong.query.join(followers, (followers.c.followed_id == AnswerLong.id_user)).filter(
            followers.c.follower_id == self.id).order_by(AnswerLong.create_date.desc())

    def followed_snippet(self):
        return Snippet.query.join(followers, (followers.c.followed_id == Snippet.id_user)).filter(
            followers.c.follower_id == self.id).order_by(Snippet.create_date.desc())



class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    skill_name = db.Column(db.String(50))


    def __init__(self, user_id, skill_name):
        self.user_id = user_id
        self.skill_name = skill_name

class Personal_User(db.Model):
    __tablename__ = 'user_personal_info'
    id = db.Column(db.Integer, primary_key=True)
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

    @property
    def get_username(self):
        username = db.session.query(User.username).filter_by(id=self.id_user).first()
        return username[0]


question_upvote = Table('question_upvote', db.metadata,
                       db.Column('user_question.id', db.Integer, db.ForeignKey('user_question.id')),
                       db.Column('upvote.id', db.Integer, db.ForeignKey('upvote.id'))
                       )


question_downvote = Table('question_downvote', db.metadata,
                          db.Column('user_question.id', db.Integer, db.ForeignKey('user_question.id')),
                          db.Column('downvote.id', db.Integer, db.ForeignKey('downvote.id'))
                          )


class Question(db.Model):
    __tablename__ = 'user_question'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    text_area = db.Column(UnicodeText)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, id_user, title, description, text_area):
        self.id_user = id_user
        self.title = title
        self.description = description
        self.text_area = text_area

    @aggregated('upvote', db.Column(db.Integer, default=0))
    def upvote_count(self):
        return func.count('1')

    @aggregated('downvote', db.Column(db.Integer, default=0))
    def downvote_count(self):
        return func.count('1')

    upvote = db.relationship('Upvote', secondary=question_upvote, backref=db.backref('users_upvote'))

    downvote = db.relationship('Downvote', secondary=question_downvote, backref=db.backref('users_downvote'))


    @property
    def get_createdate(self):
        return str(self.create_date).split(" ")[0]

    @property
    def get_username(self):
        username = db.session.query(User.username).filter_by(id=self.id_user).first()
        return username[0]


class Upvote(db.Model):
    __tablename__ = 'upvote'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Downvote(db.Model):
    __tablename__ = 'downvote'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class TagQuestion(db.Model):
    __tablename__ = 'tag_question'
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'), nullable=False)
    tag_relation = db.relationship('Question', backref=db.backref('user_question_tag',
                                                                  cascade="all, delete-orphan"), lazy='joined')
    tag_one = db.Column(db.String(25), nullable=True)
    tag_two = db.Column(db.String(25), nullable=True)
    tag_three = db.Column(db.String(25), nullable=True)

    def __init__(self, id_question, tag_one, tag_two, tag_three):
        self.id_question = id_question
        self.tag_one = tag_one
        self.tag_two = tag_two
        self.tag_three = tag_three



answer_has_upvote = Table('answer_has_upvote', db.metadata,
                        db.Column('user_answer_long.id', db.Integer, db.ForeignKey('user_answer_long.id')),
                        db.Column('answer_upvote.id', db.Integer, db.ForeignKey('answer_upvote.id'))
                        )


answer_has_downvote = Table('answer_has_downvote', db.metadata,
                          db.Column('answer_user_answer_long.id', db.Integer, db.ForeignKey('user_answer_long.id')),
                          db.Column('answer_downvote.id', db.Integer, db.ForeignKey('answer_downvote.id'))
                          )

class AnswerLong(db.Model):
    __tablename__ = 'user_answer_long'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('user_question.id'))
    question = db.relationship('Question', backref=db.backref('user_question_answer',
                                                              cascade="all, delete-orphan"), lazy='joined')
    answer = db.Column(db.String(2000), nullable=False)
    answer_code = db.Column(UnicodeText, nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, id_question, answer, answer_code):
        self.id_user = id_user
        self.id_question = id_question
        self.answer = answer
        self.answer_code = answer_code

    @aggregated('upvote', db.Column(db.Integer, default=0))
    def upvote_count(self):
        return func.count('1')

    @aggregated('downvote', db.Column(db.Integer, default=0))
    def downvote_count(self):
        return func.count('1')


    upvote = db.relationship('Answer_Upvote', secondary=answer_has_upvote, backref=db.backref('users_answer_upvote'))

    downvote = db.relationship('Answer_Downvote', secondary=answer_has_downvote, backref=db.backref('users_answer_downvote'))


    @property
    def get_createdate(self):
        return str(self.create_date).split(" ")[0]


    @property
    def get_username(self):
        username = db.session.query(User.username).filter_by(id=self.id_user).first()
        return username[0]


class Answer_Upvote(db.Model):
    __tablename__ = 'answer_upvote'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Answer_Downvote(db.Model):
    __tablename__ = 'answer_downvote'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



snippet_has_star = Table('snippet_has_star', db.metadata,
                          db.Column('user_snippet.id', db.Integer, db.ForeignKey('user_snippet.id')),
                          db.Column('star_snippet.id', db.Integer, db.ForeignKey('star_snippet.id'))
                          )


class Snippet(db.Model):
    __tablename__ = 'user_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(45))
    description = db.Column(db.String(250))
    text_area = db.Column(UnicodeText)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, title, description, text_area):
        self.id_user = id_user
        self.title = title
        self.description = description
        self.text_area = text_area

    @aggregated('star', db.Column(db.Integer, default=0))
    def star_count(self):
        return func.count('1')


    star = db.relationship('Star', secondary=snippet_has_star, backref=db.backref('users_snippet_star'))


    @property
    def get_createdate(self):
        return str(self.create_date).split(" ")[0]

    @property
    def get_username(self):
        username = db.session.query(User.username).filter_by(id=self.id_user).first()
        return username[0]


class Star(db.Model):
    __tablename__ = 'star_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class TagSnippet(db.Model):
    __tablename__ = 'tag_snippet'
    id = db.Column(db.Integer, primary_key=True)
    id_snippet = db.Column(db.Integer, db.ForeignKey('user_snippet.id'), nullable=False)
    tag_relation = db.relationship('Snippet', backref=db.backref('user_snippet_tag',
                                                                 cascade="all, delete-orphan"), lazy='joined')
    tag_one = db.Column(db.String(25), nullable=True)
    tag_two = db.Column(db.String(25), nullable=True)
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
    comment_text = db.Column(db.String(120), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id_user, id_snippet, comment_text):
        self.id_user = id_user
        self.id_snippet = id_snippet
        self.comment_text = comment_text

    @property
    def get_createdate(self):
        return str(self.create_date).split(" ")[0]

    @property
    def get_username(self):
        username = db.session.query(User.username).filter_by(id=self.id_user).first()
        return username[0]