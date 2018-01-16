from ..extensions import marshmallow

from .comment import CommentSchema

from marshmallow import fields


class SnippetCommentSchema(marshmallow.Schema):
    id = fields.Int()
    comments = fields.Nested(CommentSchema, many=True)