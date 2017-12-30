import pytest, datetime

from ...app.models import User, UserSchema, UserInformation, UserNotificationSchema, Notification
from ..factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """Test user model"""

    def test_created_defaults_to_datetime(self, db):
        user = User(username='foo', email='foo@bar.com', password='123456')
        db.session.add(user)
        db.session.commit()
        assert bool(user.created)
        assert isinstance(user.created, datetime.datetime)
        assert User.query.count() == 1

    def test_factory(self, db):
        user = UserFactory()
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created)
        assert User.query.count() == 1

    def test_password_hash(self, db):
        user = UserFactory()
        db.session.commit()
        assert user.password == '123456'
        assert user.password != '_123456'

    def test_serialization_with_marshmallow(self, db):
        user = UserFactory()
        db.session.commit()
        user_schema = UserSchema()
        user_serialized = user_schema.dump(user).data
        assert len(user_serialized) == 6
        assert user_serialized['id'] == 1
        assert user_serialized['username'] == 'user'
        assert user_serialized['email'] == 'user@example.com'
        assert isinstance(user_serialized['created'], str)
        assert isinstance(user_serialized['updated'], str)

    def test_serialization_with_marshmallow_and_user_information(self, db):
        user = UserFactory()
        db.session.commit()
        user_information = UserInformation(id_user=user.id, country="Canada", bio="Sadness")
        db.session.add(user_information)
        user_schema = UserSchema()
        user_serialized = user_schema.dump(user).data
        assert user_serialized['information']['country'] == "Canada"
        assert user_serialized['information']['bio'] == "Sadness"
        assert len(user_serialized['information']) == 2

    def test_serialized_with_marshmallow_with_notifications(self, db, user):
        _user = user.get()
        _user_should_ignore = UserFactory(username="Carl")
        db.session.commit()
        notification = Notification(id_user=_user.id, description="Carl answered your question")
        db.session.add(notification)
        notification = Notification(id_user=_user.id, description="Tomas answered your question",
                                    url="/questions/23")
        db.session.add(notification)
        notification = Notification(id_user=_user_should_ignore.id, description="Tomas answered your question")
        db.session.add(notification)
        db.session.commit()
        user_notification_schema = UserNotificationSchema()
        user_notification_serialized = user_notification_schema.dump(_user).data
        assert len(user_notification_serialized['notification']) == 2
        assert 'url' not in user_notification_serialized['notification'][0]
        assert 'url' in user_notification_serialized['notification'][1]
        user_notification_serialized = user_notification_schema.dump(_user_should_ignore).data
        assert len(user_notification_serialized['notification']) == 1
        assert 'url' not in user_notification_serialized['notification'][0]
