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

    username = 'user'
    email    = 'user@example.com'
    password = '123456'

    def __init__(self, username, email):
        username = username
        email    = email

    class Meta:
        """Factory configuration."""
        model = User