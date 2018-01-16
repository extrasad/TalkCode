from ..extensions import marshmallow
from ..utils.schema_without_none import SchemaWithoutNoneFields

from marshmallow import post_dump


class NotificationSchema(marshmallow.Schema, SchemaWithoutNoneFields):
  class Meta:
    fields = ('id', 'description', 'status', 'url', 'created', 'updated')
  
  @post_dump
  def transform_status_to_correct_value(self, in_data):
    """ Transform status value (0 or 1) to checked or unchecked """
    in_data['status'] = in_data['status'].code
    return in_data