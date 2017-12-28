"""Factories to help in tests."""
from factory import Sequence # PostGenerationMethodCall
from factory.alchemy import SQLAlchemyModelFactory

from ..app.database import db
from ..app.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = Sequence(lambda n: '123456_{0}'.format(n))
    # password = PostGenerationMethodCall('set_password', 'example') # TODO: Create set_password property

    class Meta:
        """Factory configuration."""
        model = User