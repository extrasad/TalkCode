import pytest, datetime

from ...app.models import Question, QuestionSchema, User, Upvote, Downvote
from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestQuestion:
    """Test question model"""

    def test_created_question_and_relation_with_user(self, db, user):
      _user = user.get()
      question = Question(id_user=_user.id, text="What is the life?")
      db.session.add(question)
      db.session.commit()
      Question.query.count() == 1

    def test_upvote(self, db, user):
        _user = user.get()
        question = Question(id_user=_user.id, text="What is the life?")
        db.session.add(question)
        user1 = UserFactory(username="userLike1", email="userLike1@gmail.com")
        user2 = UserFactory(username="userLike2", email="userLike2@gmail.com")
        db.session.commit()
        question.upvote.append(Upvote(id_user=user1.id))
        question.upvote.append(Upvote(id_user=user2.id))
        db.session.commit()
        assert question.upvote_count == 2
        assert question.downvote_count == 0

    def test_downvote(self, db, user):
        _user = user.get()
        question = Question(id_user=_user.id, text="What is the life?")
        db.session.add(question)
        user1 = UserFactory(username="user__1", email="user__1@gmail.com")
        user2 = UserFactory(username="user__2", email="user__2@gmail.com")
        user3 = UserFactory(username="user__3", email="user__3@gmail.com")
        db.session.commit()
        question.downvote.append(Downvote(id_user=user1.id))
        question.downvote.append(Downvote(id_user=user2.id))
        question.downvote.append(Downvote(id_user=user3.id))
        db.session.commit()
        assert question.downvote_count == 3
        assert question.upvote_count == 0

    def test_serialization_with_marshmallow(self, db, user):
        _user = user.get()
        question = Question(id_user=_user.id, text="What is the life?")
        db.session.add(question)
        user1 = UserFactory(username="user__1", email="user__1@gmail.com")
        user2 = UserFactory(username="user__2", email="user__2@gmail.com")
        user3 = UserFactory(username="user__3", email="user__3@gmail.com")
        user4 = UserFactory(username="user__4", email="user__4@gmail.com")
        user5 = UserFactory(username="user__5", email="user__5@gmail.com")
        user6 = UserFactory(username="user__6", email="user__6@gmail.com")
        db.session.commit()
        question.downvote.append(Downvote(id_user=user1.id))
        question.downvote.append(Downvote(id_user=user2.id))
        question.downvote.append(Downvote(id_user=user3.id))
        question.downvote.append(Downvote(id_user=user4.id))
        question.upvote.append(Upvote(id_user=user5.id))
        question.upvote.append(Upvote(id_user=user6.id))
        db.session.commit()
        question_schema = QuestionSchema()
        question_serialized = question_schema.dump(question).data
        assert question_serialized['upvote_count'] == 2
        assert question_serialized['downvote_count'] == 4
        assert question_serialized['id_user'] == 1
        assert question_serialized['text'] == "What is the life?"