import pytest

from ...app.models import Tag, TagSchema
from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestTag:
  """Test tag model"""
  def test_create_tag(self, db, user):
    _user = user.get()
    tag = Tag("python", "language")
    db.session.add(tag)
    db.session.commit()

    assert Tag.query.count() == 1
  
  def test_serialized_with_marshmallow(self, db, user):
    _user = user.get()
    tag = Tag("python", "language")
    db.session.add(tag)
    db.session.commit()
    tag_schema = TagSchema()
    tag_serialized = tag_schema.dump(tag).data
    assert tag_serialized['name'] == tag.name
    assert tag_serialized['description'] == tag.description
