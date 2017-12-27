from app.extensions import db
from sqlalchemy import UnicodeText

import datetime


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(350))
    description = db.Column(db.String(1000))
    text_area = db.Column(UnicodeText)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)