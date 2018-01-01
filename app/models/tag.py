from ..database import db, Model , Column
from ..extensions import marshmallow

from sqlalchemy_utils import Timestamp


class Tag(Model, Timestamp):
  __tablename__ = 'tag'
  id          = Column(db.Integer, primary_key=True)
  name        = Column(db.String(24), unique=True, nullable=False)
  description = Column(db.String(36), nullable=False)

  def __init__(self, name, description):
    self.name = name
    self.description = description
    

class TagSchema(marshmallow.Schema):
  class Meta:
    fields = ('id', 'name', 'description')