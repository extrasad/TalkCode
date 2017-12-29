from ..database import db, Model , Column, relationship
from ..extensions import marshmallow

from sqlalchemy_utils import PasswordType, EmailType, force_auto_coercion, Timestamp

import datetime, flask

force_auto_coercion()

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
    
    def __init__(self, username, email, password):
        self.username = username
        self.email    = unicode(email) # https://stackoverflow.com/questions/20091801/python-with-mysql-sawarning-unicode-type-received-non-unicode-bind-param-value
        self.password = password

class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created', 'updated')