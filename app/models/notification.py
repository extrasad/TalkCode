from ..database import db, Model , Column
from ..extensions import marshmallow
from ..utils.schema_without_none import SchemaWithoutNoneFields

from marshmallow import post_dump

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


class NotificationSchema(marshmallow.Schema, SchemaWithoutNoneFields):
  class Meta:
    fields = ('id', 'description', 'status', 'url', 'created', 'updated')
  
  @post_dump
  def transform_status_to_correct_value(self, in_data):
    """ Transform status value (0 or 1) to checked or unchecked """
    in_data['status'] = in_data['status'].code
    return in_data