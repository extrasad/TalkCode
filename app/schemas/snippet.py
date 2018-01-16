from ..utils.user_nested_exclude_list import USER_NESTED_FIELDS_EXCLUDES
from ..extensions import marshmallow

from .tag import TagSchema
from .user import UserSchema

from marshmallow import fields


class SnippetSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'filename', 'body', 'description',
                  'star_count', 'tags', 'created', 'updated',
                  'user')
    
    id = fields.Int()
    star_count = fields.Int()
    tags = fields.Nested(TagSchema, many=True)
    user = fields.Nested(UserSchema, exclude=USER_NESTED_FIELDS_EXCLUDES)
    # TODO: Add comment field nested SnippetCommentSchema