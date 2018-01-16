from ..database import db, Model , Column

from sqlalchemy_utils import Timestamp, ChoiceType


class Notification(Model, Timestamp):
  STATUS = [
    (u'checked', u'0'),
    (u'unchecked', u'1')
  ]

  __tablename__ = 'notification'
  id          = Column(db.Integer, primary_key=True)
  id_user     = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  description = Column(db.String(85), nullable=False)
  url         = Column(db.String(128), nullable=True)
  status      = Column(ChoiceType(STATUS), nullable=False, default=u'unchecked')

  def __init__(self, id_user, description, status=None, url=None):
    self.id_user     = id_user
    self.description = description
    self.status      = status
    self.url         = url