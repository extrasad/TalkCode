from ..database import db, Model, Column


class Star(Model):
    __tablename__ = 'star'
    id      = Column(db.Integer, primary_key=True)
    id_user = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)