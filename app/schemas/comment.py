from ..utils.user_nested_exclude_list import USER_NESTED_FIELDS_EXCLUDES
from ..extensions import marshmallow

from .user import UserSchema

from marshmallow import fields


class CommentSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'text', 'created', 'updated', 'user')

    id = fields.Int()
    user = fields.Nested(UserSchema, exclude=USER_NESTED_FIELDS_EXCLUDES)