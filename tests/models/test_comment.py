import pytest

from ...app.models import Snippet, Comment, CommentSchema
from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestNotification:
  """Test comment snippet model"""

  def test_create_comment(self, db, user):
    _user_snippet = user.get()
    _user_comment = UserFactory(username="the_comment_man")
    snippet = Snippet(id_user=_user_snippet.id, filename="application.rb",
                      body="lorem ipsum")
    db.session.add(snippet)
    db.session.commit()
    snippet_comment = Comment(_user_comment.id, snippet.id, 'This is a comment')
    db.session.add(snippet_comment)
    db.session.commit()

    assert Comment.query.count() == 1

  def test_search_user_comment_name(self, db, user):
    _user_snippet = user.get()
    _user_comment = UserFactory(username="the_comment_man")
    snippet = Snippet(id_user=_user_snippet.id, filename="application.rb",
                      body="lorem ipsum")
    db.session.add(snippet)
    db.session.commit()
    snippet_comment = Comment(_user_comment.id, snippet.id, 'This is a comment')
    db.session.add(snippet_comment)
    db.session.commit()
    assert snippet_comment.user.username == 'the_comment_man'

  def test_serialized_with_marshmallow(self, db, user):
    _user_snippet = user.get()
    _user_comment = UserFactory(username="the_comment_man")
    snippet = Snippet(id_user=_user_snippet.id, filename="application.rb",
                      body="lorem ipsum")
    db.session.add(snippet)
    db.session.commit()
    snippet_comment = Comment(_user_comment.id, snippet.id, 'This is a comment')
    db.session.add(snippet_comment)
    db.session.commit()
    comment_schema = CommentSchema()
    comment_serialized = comment_schema.dump(snippet_comment).data
    print comment_serialized
    assert 'created' in comment_serialized
    assert 'updated' in comment_serialized
    assert comment_serialized['id'] == 1
    assert comment_serialized['text'] == 'This is a comment'
    assert comment_serialized['user']['id'] == 2
    assert comment_serialized['user']['email'] == 'user@example.com'
    assert 'created' not in comment_serialized['user']
    assert 'updated' not in comment_serialized['user']
    assert 'information' not in comment_serialized['user']
    