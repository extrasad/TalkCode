from ..database import db, Model, Column

class Downvote(db.Model):
    __tablename__ = 'downvote'
    id      = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)