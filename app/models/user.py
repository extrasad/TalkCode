from ..database import db, Model , Column, relationship
from ..extensions import marshmallow
from .user_information import UserInformationSchema
from .notification import NotificationSchema

from sqlalchemy_utils import PasswordType, EmailType, force_auto_coercion, Timestamp, aggregated, QueryChain
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


from marshmallow import fields

import datetime, flask

force_auto_coercion()

# Many to Many Relationship betweeen User and Followers

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(Model, Timestamp):
    __tablename__ = 'user'
    id       = Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True)
    email    = Column(EmailType)
    password = Column(
        PasswordType(
            # The returned dictionary is forwarded to the CryptContext
            onload=lambda **kwargs: dict(
                schemes=flask.current_app.config['PASSWORD_SCHEMES'],
                **kwargs
            ),
        ),
        unique=False,
        nullable=False,
    )

    # Validations

    @validates('username')
    def validate_username(self, key, username):
        from ..controllers.interface.authentication.descriptions import SIGN_UP_DESCRIPTIONS as _
        if len(username) <= 2:
            raise ValueError(_['INVALID_USERNAME'])
        else:
            return username

    @validates('password')
    def validate_password(self, key, password):
        from ..controllers.interface.authentication.descriptions import SIGN_UP_DESCRIPTIONS as _
        if len(password) <= 5:
            raise ValueError(_['INVALID_PASSWORD'])
        else:
            return password

    @validates('email')
    def validate_email(self, key, address):
        from ..controllers.interface.authentication.descriptions import SIGN_UP_DESCRIPTIONS as _
        if len(address) < 3 or '@' not in address:
            raise ValueError(_['INVALID_EMAIL'])
        else:
            return address

    # Aggregateds
    
    @aggregated('comments', db.Column(db.Integer, default=0))
    def comments_count(self):
        return db.func.count('1')

    @aggregated('answers', db.Column(db.Integer, default=0))
    def answers_count(self):
        return db.func.count('1')

    @aggregated('questions', db.Column(db.Integer, default=0))
    def questions_count(self):
        return db.func.count('1')

    @aggregated('snippets', db.Column(db.Integer, default=0))
    def snippets_count(self):
        return db.func.count('1')

    # Relationships

    information  = relationship('UserInformation', uselist=False)
    notification = relationship('Notification', backref='notifications')
    comments     = relationship("Comment", back_populates="user")
    answers      = relationship("Answer", back_populates="user")
    snippets     = relationship("Snippet", back_populates="user")
    questions    = relationship("Question", back_populates="user")
    followed     = relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')

    @hybrid_property
    def stars_total_count(self):
        from ..models import Snippet
        return db.session.query(db.func.sum(Snippet.star_count)).filter_by(id_user=self.id).scalar() or 0

    @hybrid_property
    def upvotes_total_count(self):
        from ..models import Question
        return db.session.query(db.func.sum(Question.upvote_count)).filter_by(id_user=self.id).scalar() or 0

    @hybrid_property
    def downvotes_total_count(self):
        from ..models import Question
        return db.session.query(db.func.sum(Question.downvote_count)).filter_by(id_user=self.id).scalar() or 0

    @hybrid_property
    def followed_count(self):
        return self.followed.count()

    @hybrid_property
    def followers_count(self):
        return self.followers.count()

    def __init__(self, username, email, password):
        self.username = username
        self.email    = unicode(email) # https://stackoverflow.com/questions/20091801/python-with-mysql-sawarning-unicode-type-received-non-unicode-bind-param-value
        self.password = password

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def followed_resource(self, cls):
        # TODO: Add limit parameter
        return cls.query.join(followers, (followers.c.followed_id == cls.id_user)).filter(
            followers.c.follower_id == self.id).order_by(cls.created.desc())

    def encode_auth_token(self):
        import jwt
        try:
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5)
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(payload, flask.current_app.config['SIGNING_KEY'], algorithm='RS256'), exp
        except Exception as e:
            return e


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created', 'updated',
                  'followed_count', 'followers_count', 'information',
                  'comments_count', 'snippets_count', 'questions_count',
                  'answers_count', 'stars_total_count', 'upvotes_total_count',
                  'downvotes_total_count')
    
    id = fields.Int()
    followed_count = fields.Int()
    followers_count = fields.Int()
    comments_count = fields.Int()
    snippets_count = fields.Int()
    questions_count = fields.Int()
    answers_count = fields.Int()
    stars_total_count = fields.Int()
    upvotes_total_count = fields.Int()
    downvotes_total_count = fields.Int()
    information = marshmallow.Nested(UserInformationSchema)


class UserNotificationSchema(marshmallow.Schema):
    id = fields.Str()
    notification = fields.Nested(NotificationSchema, many=True, exclude=[u'updated'])


class AuthorizedPayLoadSchema(marshmallow.Schema):
    class Meta:
        fields = ('idToken', 'expiresIn', 'user')
        
    idToken = fields.Str()
    expiresIn = fields.Str()
    user = marshmallow.Nested(UserSchema)