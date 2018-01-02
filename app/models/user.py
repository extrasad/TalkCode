from ..database import db, Model , Column, relationship
from ..extensions import marshmallow
from .user_information import UserInformationSchema
from .notification import NotificationSchema

from sqlalchemy_utils import PasswordType, EmailType, force_auto_coercion, Timestamp, aggregated
from sqlalchemy.ext.hybrid import hybrid_property

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
    # Relationships
    information  = relationship('UserInformation', uselist=False)
    notification = relationship('Notification', backref='notifications')
    comments     = relationship("Comment", back_populates="user")
    answers      = relationship("Answer", back_populates="user")
    followed     = relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')

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
        return cls.query.join(followers, (followers.c.followed_id == cls.id_user)).filter(
            followers.c.follower_id == self.id).order_by(cls.created.desc())


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created', 'updated', 'followed_count', 'followers_count', 'information')
    
    id = fields.Int()
    followed_count = fields.Int()
    followers_count = fields.Int()
    information = marshmallow.Nested(UserInformationSchema)


class UserNotificationSchema(marshmallow.Schema):
    id = fields.Str()
    notification = fields.Nested(NotificationSchema, many=True, exclude=[u'updated'])