from app.extensions import db

import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(66))
    username = db.Column(db.String(80), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)