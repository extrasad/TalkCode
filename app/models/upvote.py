from ..database import db, Model, Column, relationship, backref, metadata

class Upvote(db.Model):
    __tablename__ = 'upvote'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)