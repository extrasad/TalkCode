from ..extensions import marshmallow

from .question import QuestionSchema

from marshmallow import fields


class UserQuestionSchema(marshmallow.Schema):
    id = fields.Str()
    questions = fields.Nested(QuestionSchema, many=True, exclude=[u'updated' , u'user'])