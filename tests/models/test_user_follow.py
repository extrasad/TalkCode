import pytest, datetime

from ...app.models import User, Snippet, Question, Answer
from ..factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUserFollow:
    """Test user followers and followed relationships"""

    def test_user_follow_others_user(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      db.session.commit()
      assert len(_user.followed.all()) == 0
      _user.follow(user_followed_1)
      _user.follow(user_followed_2)
      assert len(_user.followed.all()) == 2


    def test_user_unfollow_others_user(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      db.session.commit()
      assert len(_user.followed.all()) == 0
      _user.followed.append(user_followed_1)
      _user.followed.append(user_followed_2)
      assert len(_user.followed.all()) == 2
      _user.unfollow(user_followed_1)
      _user.unfollow(user_followed_2)
      assert len(_user.followed.all()) == 0

    def test_count_followers(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      db.session.commit()
      assert len(_user.followed.all()) == 0
      user_followed_1.follow(_user)
      assert len(_user.followers.all()) == 1
      user_followed_2.follow(_user)
      assert len(_user.followers.all()) == 2
      assert _user.followers.count() == 2

    def test_count_followed(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      db.session.commit()
      _user.followed.append(user_followed_1)
      _user.followed.append(user_followed_2)
      assert _user.followed.count() == 2

    def test_user_get_snippets_of_following(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      user_followed_3 = UserFactory(username="user__3", email="user__3@gmail.com")
      db.session.commit()
      snippet_1 = Snippet(id_user=user_followed_1.id, filename="application.rb",
                        body="lorem ipsum", description="lorem ipsum edsum")
      snippet_2 = Snippet(id_user=user_followed_1.id, filename="application.rb",
                          body="lorem ipsum", description="lorem ipsum edsum")
      snippet_3 = Snippet(id_user=user_followed_2.id, filename="application.rb",
                          body="lorem ipsum", description="lorem ipsum edsum")
      snippet_4 = Snippet(id_user=user_followed_3.id, filename="application.rb",
                          body="lorem ipsum", description="lorem ipsum edsum")
      db.session.add(snippet_1)
      db.session.add(snippet_2)
      db.session.add(snippet_3)
      db.session.add(snippet_4)
      db.session.commit()
      assert len(_user.followed_resource(Snippet).all()) == 0
      _user.followed.append(user_followed_1)
      _user.followed.append(user_followed_2)
      assert len(_user.followed_resource(Snippet).all()) == 3

    def test_user_get_questions_of_following(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      user_followed_3 = UserFactory(username="user__3", email="user__3@gmail.com")
      db.session.commit()
      question_1 = Question(id_user=user_followed_1.id, text="What is the life?")
      question_2 = Question(id_user=user_followed_2.id, text="What is the life?")
      question_3 = Question(id_user=user_followed_3.id, text="What is the life?")
      db.session.add(question_1)
      db.session.add(question_2)
      db.session.add(question_3)
      db.session.commit()
      assert len(_user.followed_resource(Question).all()) == 0
      _user.followed.append(user_followed_1)
      _user.followed.append(user_followed_2)
      assert len(_user.followed_resource(Question).all()) == 2

    def test_user_get_answers_of_following(self, db, user):
      _user = user.get()
      user_followed_1 = UserFactory(username="user__1", email="user__1@gmail.com")
      user_followed_2 = UserFactory(username="user__2", email="user__2@gmail.com")
      db.session.commit()
      question = Question(id_user=user_followed_1.id, text="What is the life?")
      db.session.add(question)
      db.session.commit()
      answer = Answer(user_followed_2.id, question.id, "Answer?")
      db.session.add(answer)
      db.session.commit()
      assert len(_user.followed_resource(Answer).all()) == 0
      _user.followed.append(user_followed_1)
      _user.followed.append(user_followed_2)
      assert len(_user.followed_resource(Answer).all()) == 1
      assert _user.followed_resource(Answer).all()[0].id_user == user_followed_2.id

    # def test_user_follow_serialize(self, db, user):
        