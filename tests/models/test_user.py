import pytest, datetime

from ...app.models import User, UserSchema
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
        assert len(user_serialized) == 5
        assert user_serialized['id'] == 1
        assert user_serialized['username'] == 'user'
        assert user_serialized['email'] == 'user@example.com'
        assert isinstance(user_serialized['created'], str)
        assert isinstance(user_serialized['updated'], str)