from ..extensions import marshmallow

from .notification import NotificationSchema

from marshmallow import fields


class UserNotificationSchema(marshmallow.Schema):
    id = fields.Str()
    notification = fields.Nested(NotificationSchema, many=True, exclude=[u'updated'])