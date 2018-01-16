from ..extensions import marshmallow

from .user import UserSchema

from marshmallow import fields


class AuthorizedPayLoadSchema(marshmallow.Schema):
    class Meta:
        fields = ('idToken', 'expiresIn', 'user')
        
    idToken = fields.Str()
    expiresIn = fields.Str()
    user = marshmallow.Nested(UserSchema)