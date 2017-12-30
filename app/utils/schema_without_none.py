from marshmallow import Schema, fields, post_dump

class SchemaWithoutNoneFields(Schema):
  """Prevent serialized fields that have None value"""
  SKIP_VALUES = set([None])

  @post_dump
  def remove_skip_values(self, data):
      return {
          key: value for key, value in data.items()
          if value not in self.SKIP_VALUES
      }