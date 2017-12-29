from ..database import db, Model, Column, relationship, backref, metadata
from ..extensions import marshmallow

from sqlalchemy_utils import Timestamp, aggregated
from sqlalchemy import UnicodeText, Table, func

# Many to Many Relationship betweeen Question and Upvote/DownVote

question_upvote = Table('question_upvote', metadata,
                       Column('question.id', db.Integer, db.ForeignKey('question.id')),
                       Column('upvote.id', db.Integer, db.ForeignKey('upvote.id')))


question_downvote = Table('question_downvote', metadata,
                          Column('question.id', db.Integer, db.ForeignKey('question.id')),
                          Column('downvote.id', db.Integer, db.ForeignKey('downvote.id')))


class Question(Model, Timestamp):
    __tablename__ = 'question'
    id      = Column(db.Integer, primary_key=True)
    id_user = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text    = Column(UnicodeText(2048), nullable=False)

    @aggregated('upvote', db.Column(db.Integer, default=0))
    def upvote_count(self):
        return func.count('1')

    @aggregated('downvote', db.Column(db.Integer, default=0))
    def downvote_count(self):
        return func.count('1')

    upvote = relationship('Upvote',
        secondary=question_upvote,
        backref=backref('users_upvote'))

    downvote = relationship('Downvote',
        secondary=question_downvote,
        backref=backref('users_downvote'))
    

    def __init__(self, id_user, text):
        self.id_user  = id_user
        self.text     = unicode(text)


class QuestionSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'id_user', 'text', 'upvote_count', 'downvote_count', 'created', 'updated')