from ..extensions import marshmallow

from .user_information import UserInformationSchema

from marshmallow import fields


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created', 'updated',
                  'followed_count', 'followers_count', 'information',
                  'comments_count', 'snippets_count', 'questions_count',
                  'answers_count', 'stars_total_count', 'upvotes_total_count',
                  'downvotes_total_count')
    
    id = fields.Int()
    followed_count = fields.Int()
    followers_count = fields.Int()
    comments_count = fields.Int()
    snippets_count = fields.Int()
    questions_count = fields.Int()
    answers_count = fields.Int()
    stars_total_count = fields.Int()
    upvotes_total_count = fields.Int()
    downvotes_total_count = fields.Int()
    information = marshmallow.Nested(UserInformationSchema)