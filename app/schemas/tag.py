from ..extensions import marshmallow

from marshmallow import fields


class TagSchema(marshmallow.Schema):
  class Meta:
    fields = ('id', 'name', 'description')

  id = fields.Int()