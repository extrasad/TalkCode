from ..utils.user_nested_exclude_list import USER_NESTED_FIELDS_EXCLUDES
from ..extensions import marshmallow

from .user import UserSchema

from marshmallow import fields


class AnswerSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'id_question', 'text', 'created',
                  'updated', 'upvote_count', 'downvote_count',
                  'user')

    id = fields.Int()
    upvote_count = fields.Int()
    downvote_count = fields.Int()
    user = fields.Nested(UserSchema, exclude=USER_NESTED_FIELDS_EXCLUDES)