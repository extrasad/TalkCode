from ..database import db, Model , Column, relationship, metadata

from sqlalchemy import UnicodeText, Table, func
from sqlalchemy.orm import validates
from sqlalchemy_utils import Timestamp, aggregated

# Many to Many Relationship betweeen Snippet and Star

snippet_has_star = Table('snippet_has_star', metadata,
                          db.Column('snippet.id', db.Integer, db.ForeignKey('snippet.id')),
                          db.Column('star.id', db.Integer, db.ForeignKey('star.id')))

snippet_has_tag = Table('snippet_has_tag', metadata,
                          db.Column('snippet.id', db.Integer, db.ForeignKey('snippet.id')),
                          db.Column('tag.id', db.Integer, db.ForeignKey('tag.id')))


class Snippet(Model, Timestamp):
    __tablename__ = 'snippet'
    id          = Column(db.Integer, primary_key=True)
    id_user     = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename    = Column(db.String(60), nullable=False)
    body        = Column(UnicodeText, nullable=False)
    description = Column(db.String(100*24), nullable=True)
    # Relationships
    comments    = relationship('Comment', backref='snippets')
    tags        = relationship("Tag", secondary=snippet_has_tag)
    user        = relationship("User", back_populates="snippets")

    @aggregated('star', Column(db.Integer, default=0))
    def star_count(self):
        return func.count('1')

    star = db.relationship('Star', secondary=snippet_has_star, backref=db.backref('users_snippet_star'))

    @validates('filename')
    def validate_file_format(self, key, filename):
        import re
        pattern = r'^[\w,\s-]+\.[A-Za-z]{1,6}$'
        assert re.match(pattern, filename)
        return filename


    def __init__(self, id_user, filename, body, description=None):
        self.id_user     = id_user
        self.filename    = filename
        self.body        = unicode(body)
        self.description = unicode(description)