from ..utils.user_nested_exclude_list import USER_NESTED_FIELDS_EXCLUDES
from ..extensions import marshmallow

from .user import UserSchema

from marshmallow import fields


class QuestionSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'text', 'upvote_count',
                  'downvote_count', 'created', 'updated',
                  'user')
    
    id = fields.Int()
    upvote_count = fields.Int()
    downvote_count = fields.Int()
    user = fields.Nested(UserSchema, exclude=USER_NESTED_FIELDS_EXCLUDES)