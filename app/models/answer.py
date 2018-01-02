from ..database import db, Model , Column, relationship, metadata, backref
from ..extensions import marshmallow
from ..utils.schema_without_none import SchemaWithoutNoneFields

from .user import UserSchema

from marshmallow import fields

from sqlalchemy import UnicodeText, Table, func
from sqlalchemy_utils import Timestamp, aggregated


answer_upvote = Table('answer_upvote', metadata,
                       Column('answer.id', db.Integer, db.ForeignKey('answer.id')),
                       Column('upvote.id', db.Integer, db.ForeignKey('upvote.id')))


answer_downvote = Table('answer_downvote', metadata,
                        Column('answer.id', db.Integer, db.ForeignKey('answer.id')),
                        Column('downvote.id', db.Integer, db.ForeignKey('downvote.id')))


class Answer(Model, Timestamp):
    __tablename__ = 'answer'
    id           = Column(db.Integer, primary_key=True)
    id_user      = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_question  = Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text         = Column(db.String(2048 / 2), nullable=False)
    # Relationships
    user         = relationship("User", back_populates="answers")

    @aggregated('upvote', db.Column(db.Integer, default=0))
    def upvote_count(self):
        return func.count('1')

    @aggregated('downvote', db.Column(db.Integer, default=0))
    def downvote_count(self):
        return func.count('1')

    upvote = relationship('Upvote', secondary=answer_upvote)
    downvote = relationship('Downvote', secondary=answer_downvote)

    def __init__(self, id_user, id_question, text):
        self.id_user     = id_user
        self.id_question = id_question
        self.text        = unicode(text)


class AnswerSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'id_question', 'text', 'created',
                  'updated', 'upvote_count', 'downvote_count', 'user')

    id = fields.Int()
    upvote_count = fields.Int()
    downvote_count = fields.Int()
    user = fields.Nested(UserSchema, exclude=[u'created', u'updated', u'information',
                                              u'followed_count', u'followers_count'])