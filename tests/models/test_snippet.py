import pytest, datetime

from ...app.models import Snippet, SnippetSchema, User, Star
from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestSnippet:
    """Test snippet model"""

    def test_created_snippet_and_relation_with_user(self, db, user):
      _user = user.get()
      snippet = Snippet(id_user=_user.id, filename="application.rb",
                        body="lorem ipsum", description="lorem ipsum")
      db.session.add(snippet)
      db.session.commit()
      assert Snippet.query.count() == 1

    def test_validation_filename_raise_error(self, db, user):
      _user = user.get()

      with pytest.raises(AssertionError):
        snippet = Snippet(id_user=_user.id, filename="applicatio.",
                          body="lorem ipsum", description="lorem ipsum")

      with pytest.raises(AssertionError):
        snippet = Snippet(id_user=_user.id, filename="application.",
                          body="lorem ipsum", description="lorem ipsum")

      snippet = Snippet(id_user=_user.id, filename="application.rb",
                        body="lorem ipsum", description="lorem ipsum")

      db.session.add(snippet)
      db.session.commit()
      assert Snippet.query.count() == 1

    def test_star(self, db, user):
      _user = user.get()
      snippet = Snippet(id_user=_user.id, filename="application.rb",
                        body="lorem ipsum", description="lorem ipsum")
      db.session.add(snippet)
      user1 = UserFactory(username="userLike1", email="userLike1@gmail.com")
      user2 = UserFactory(username="userLike2", email="userLike2@gmail.com")
      user3 = UserFactory(username="userLike3", email="userLike3@gmail.com")
      db.session.commit()
      snippet.star.append(Star(id_user=user1.id))
      snippet.star.append(Star(id_user=user2.id))
      snippet.star.append(Star(id_user=user3.id))
      db.session.commit()
      assert snippet.star_count == 3
      snippet.star.remove(Star.query.filter_by(id_user=user2.id).first())
      db.session.commit()
      assert snippet.star_count == 2

    def test_serialization_with_marshmallow(self, db, user):
      _user = user.get()
      snippet = Snippet(id_user=_user.id, filename="application.rb",
                        body="lorem ipsum", description="lorem ipsum edsum")
      db.session.add(snippet)
      user1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user2 = UserFactory(username="user__2", email="user__2@gmail.com")
      user3 = UserFactory(username="user__3", email="user__3@gmail.com")
      user4 = UserFactory(username="user__4", email="user__4@gmail.com")
      db.session.commit()
      snippet.star.append(Star(id_user=user1.id))
      snippet.star.append(Star(id_user=user2.id))
      snippet.star.append(Star(id_user=user3.id))
      snippet.star.append(Star(id_user=user4.id))
      db.session.commit()
      snippet_schema = SnippetSchema()
      snippet_serialized = snippet_schema.dump(snippet).data
      assert snippet_serialized['id_user'] == 1
      assert snippet_serialized['description'] == "lorem ipsum edsum"
      assert snippet_serialized['filename'] == "application.rb"
      assert snippet_serialized['body'] == "lorem ipsum"
      assert snippet_serialized['star_count'] == 4

    def test_create_snippet_without_description(self, db, user):
      _user = user.get()
      snippet = Snippet(id_user=_user.id, filename="application.rb",
                        body="lorem ipsum")
      db.session.add(snippet)
      db.session.commit()
      snippet_schema = SnippetSchema()
      snippet_serialized = snippet_schema.dump(snippet).data
      assert snippet_serialized['id_user'] == 1
      assert snippet_serialized['description'] == "None"
      assert snippet_serialized['filename'] == "application.rb"
      assert snippet_serialized['body'] == "lorem ipsum"
      assert snippet_serialized['star_count'] == 0