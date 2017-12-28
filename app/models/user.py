from ..database import db, Model , Column, relationship

import datetime


class User(Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(120), unique=True)
    password = Column(db.String(66))
    username = Column(db.String(80), unique=True)
    created_at = Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password