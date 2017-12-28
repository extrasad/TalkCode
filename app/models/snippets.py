from ..database import db, Model , Column, relationship
from sqlalchemy import UnicodeText

import datetime


class Snippet(Model):
    __tablename__ = 'snippet'
    id = Column(db.Integer, primary_key=True)
    id_user = Column(db.Integer, db.ForeignKey('user.id'))
    title = Column(db.String(45))
    description = Column(db.String(250))
    text_area = Column(UnicodeText)
    create_date = Column(db.DateTime, default=datetime.datetime.now)
