import pytest

import datetime as dt

from ...app.models import User
from ..factories import UserFactory

@pytest.mark.usefixtures('db')
class TestUser:
    """Test user model"""

    def test_created_at_defaults_to_datetime(self, db):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com', password='123456')
        db.session.add(user)
        db.session.commit()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)
        assert User.query.count() == 1

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory()
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert User.query.count() != 0