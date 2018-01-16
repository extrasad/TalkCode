import pytest

from ...app.models import Question, Answer, Upvote, Downvote
from ...app.schemas.answer import AnswerSchema

from ..factories import UserFactory


@pytest.mark.usefixtures('db', 'user')
class TestQuestion:
  """Test answer model"""
  def test_create_answer_and_relationship(self, db, user):
    _user_question = user.get()
    _user_anwswer =  UserFactory(username="user_answer", email="user_answer@gmail.com")
    question = Question(id_user=_user_question.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    answer = Answer(_user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()
    assert Answer.query.count() == 1

  def test_upvote(self, db, user):
    _user = user.get()
    question = Question(id_user=_user.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    _user_anwswer = UserFactory(username="user_answer", email="user_answer@gmail.com")
    db.session.commit()
    answer = Answer(_user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()
    user1 = UserFactory(username="userLike1", email="userLike1@gmail.com")
    user2 = UserFactory(username="userLike2", email="userLike2@gmail.com")
    db.session.commit()
    answer.upvote.append(Upvote(id_user=user1.id))
    answer.upvote.append(Upvote(id_user=user2.id))
    db.session.commit()
    assert answer.upvote_count == 2
    assert answer.downvote_count == 0

  def test_downvote(self, db, user):
    _user = user.get()
    question = Question(id_user=_user.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    _user_anwswer = UserFactory(username="user_answer", email="user_answer@gmail.com")
    db.session.commit()
    answer = Answer(_user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()
    user1 = UserFactory(username="user__1", email="user__1@gmail.com")
    user2 = UserFactory(username="user__2", email="user__2@gmail.com")
    user3 = UserFactory(username="user__3", email="user__3@gmail.com")
    db.session.commit()
    answer.downvote.append(Downvote(id_user=user1.id))
    answer.downvote.append(Downvote(id_user=user2.id))
    answer.downvote.append(Downvote(id_user=user3.id))
    db.session.commit()
    assert answer.downvote_count == 3
    assert answer.upvote_count == 0

  def test_check_not_error_if_question_and_answer_have_votes(self, db, user):
    _user = user.get()
    question = Question(id_user=_user.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    _user_anwswer = UserFactory(username="user_answer", email="user_answer@gmail.com")
    db.session.commit()
    answer = Answer(_user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()
    user1 = UserFactory(username="user__1", email="user__1@gmail.com")
    user2 = UserFactory(username="user__2", email="user__2@gmail.com")
    user3 = UserFactory(username="user__3", email="user__3@gmail.com")
    user4 = UserFactory(username="user__4", email="user__4@gmail.com")
    user5 = UserFactory(username="user__5", email="user__5@gmail.com")
    db.session.commit()
    answer.downvote.append(Downvote(id_user=user1.id))
    answer.downvote.append(Downvote(id_user=user2.id))
    answer.downvote.append(Downvote(id_user=user3.id))
    answer.upvote.append(Upvote(id_user=user1.id))
    answer.upvote.append(Upvote(id_user=user2.id))
    question.upvote.append(Upvote(id_user=user2.id))
    question.upvote.append(Upvote(id_user=user5.id))
    question.upvote.append(Upvote(id_user=user4.id))
    question.upvote.append(Upvote(id_user=user3.id))
    question.downvote.append(Downvote(id_user=user1.id))
    question.downvote.append(Downvote(id_user=user2.id))
    db.session.commit()
    assert answer.downvote_count == 3
    assert answer.upvote_count == 2
    assert question.downvote_count == 2
    assert question.upvote_count == 4

  def test_serialization_with_marshmallow(self, db, user):
    _user = user.get()
    question = Question(id_user=_user.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    _user_anwswer = UserFactory(username="user_answer", email="user_answer@gmail.com")
    db.session.commit()
    answer = Answer(_user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()
    user1 = UserFactory(username="user__1", email="user__1@gmail.com")
    user2 = UserFactory(username="user__2", email="user__2@gmail.com")
    user3 = UserFactory(username="user__3", email="user__3@gmail.com")
    db.session.commit()
    answer.downvote.append(Downvote(id_user=user1.id))
    answer.downvote.append(Downvote(id_user=user2.id))
    answer.downvote.append(Downvote(id_user=user3.id))
    answer.upvote.append(Upvote(id_user=user1.id))
    answer.upvote.append(Upvote(id_user=user2.id))
    db.session.commit()
    answer_schema = AnswerSchema()
    answer_serialized = answer_schema.dump(answer).data
    assert answer_serialized['upvote_count'] == 2
    assert answer_serialized['downvote_count'] == 3
    assert answer_serialized['id_question'] == question.id
    assert answer_serialized['text'] == "Answer?"
    assert answer_serialized['user']['id'] == _user_anwswer.id
    assert answer_serialized['user']['username'] == _user_anwswer.username
    assert answer_serialized['user']['email'] == _user_anwswer.email