from ..extensions import marshmallow

from .snippet import SnippetSchema

from marshmallow import fields


class UserSnippetSchema(marshmallow.Schema):
    id = fields.Str()
    snippets = fields.Nested(SnippetSchema, many=True, exclude=[u'updated' , u'user'])