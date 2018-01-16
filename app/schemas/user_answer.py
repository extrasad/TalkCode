from ..extensions import marshmallow

from .answer import AnswerSchema

from marshmallow import fields


class UserAnswerSchema(marshmallow.Schema):
    id = fields.Str()
    answers = fields.Nested(AnswerSchema, many=True, exclude=[u'updated' , u'user'])