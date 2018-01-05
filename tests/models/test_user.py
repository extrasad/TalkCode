import pytest, datetime

from ...app.models import *
from ..factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """Test user model"""

    def test_create_and_count(self, db):
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
    
    def test_stars_total_count(self, db):
        user = UserFactory()
        db.session.commit()
        user1 = UserFactory(username="user__1", email="user__1@gmail.com")
        user2 = UserFactory(username="user__2", email="user__2@gmail.com")
        user3 = UserFactory(username="user__3", email="user__3@gmail.com")
        user4 = UserFactory(username="user__4", email="user__4@gmail.com")
        db.session.commit()
        snippet_1 = Snippet(user.id, 'filename.py', 'lorem ipsum')
        snippet_2 = Snippet(user.id, 'filename.py', 'lorem ipsum')
        snippet_3_should_ignore = Snippet(user1.id, 'filename.py', 'lorem ipsum')
        db.session.add(snippet_1)
        db.session.add(snippet_2)
        db.session.add(snippet_3_should_ignore)
        db.session.commit()
        assert user.stars_total_count == 0
        snippet_1.star.append(Star(id_user=user1.id))
        snippet_1.star.append(Star(id_user=user2.id))
        snippet_1.star.append(Star(id_user=user3.id))
        snippet_1.star.append(Star(id_user=user4.id))
        snippet_2.star.append(Star(id_user=user3.id))
        snippet_2.star.append(Star(id_user=user4.id))
        snippet_3_should_ignore.star.append(Star(id_user=user4.id))
        assert user.stars_total_count == 6

    def test_upvotes_total_count(self, db):
        user = UserFactory()
        db.session.commit()
        user1 = UserFactory(username="user__1", email="user__1@gmail.com")
        user2 = UserFactory(username="user__2", email="user__2@gmail.com")
        user3 = UserFactory(username="user__3", email="user__3@gmail.com")
        user4 = UserFactory(username="user__4", email="user__4@gmail.com")
        db.session.commit()
        question_1 = Question(user.id, 'Wat')
        question_2 = Question(user.id, 'Wat')
        question_3_should_ignore = Question(user1.id, 'Wat')
        db.session.add(question_1)
        db.session.add(question_2)
        db.session.add(question_3_should_ignore)
        db.session.commit()
        assert user.upvotes_total_count == 0
        question_1.upvote.append(Upvote(id_user=user1.id))
        question_1.upvote.append(Upvote(id_user=user2.id))
        question_1.upvote.append(Upvote(id_user=user3.id))
        question_1.upvote.append(Upvote(id_user=user4.id))
        question_2.upvote.append(Upvote(id_user=user3.id))
        question_2.upvote.append(Upvote(id_user=user4.id))
        question_3_should_ignore.upvote.append(Upvote(id_user=user4.id))
        assert user.upvotes_total_count == 6

    def test_downvotes_total_count(self, db):
        user = UserFactory()
        db.session.commit()
        user1 = UserFactory(username="user__1", email="user__1@gmail.com")
        user2 = UserFactory(username="user__2", email="user__2@gmail.com")
        user3 = UserFactory(username="user__3", email="user__3@gmail.com")
        user4 = UserFactory(username="user__4", email="user__4@gmail.com")
        db.session.commit()
        question_1 = Question(user.id, 'Wat')
        question_2 = Question(user.id, 'Wat')
        question_3_should_ignore = Question(user1.id, 'Wat')
        db.session.add(question_1)
        db.session.add(question_2)
        db.session.add(question_3_should_ignore)
        db.session.commit()
        assert user.downvotes_total_count == 0
        question_1.downvote.append(Downvote(id_user=user1.id))
        question_1.downvote.append(Downvote(id_user=user2.id))
        question_1.downvote.append(Downvote(id_user=user3.id))
        question_1.downvote.append(Downvote(id_user=user4.id))
        question_2.downvote.append(Downvote(id_user=user3.id))
        question_2.downvote.append(Downvote(id_user=user4.id))
        question_3_should_ignore.upvote.append(Upvote(id_user=user4.id))
        assert user.downvotes_total_count == 6

    def test_serialization_with_marshmallow(self, db):
        user = UserFactory()
        db.session.commit()
        snippet_1 = Snippet(user.id, 'filename.py', 'lorem ipsum')
        snippet_2 = Snippet(user.id, 'filename.py', 'lorem ipsum')
        db.session.add(snippet_1)
        db.session.add(snippet_2)
        question_1 = Question(user.id, 'Who is god?')
        question_2 = Question(user.id, 'Who is god?')
        question_3 = Question(user.id, 'Who is god?')
        db.session.add(question_1)
        db.session.add(question_2)
        db.session.add(question_3)
        db.session.commit()
        user_schema = UserSchema()
        comment_1 = Comment(user.id, snippet_1.id, 'Wow')
        db.session.add(comment_1)
        db.session.commit()
        answer_1 = Answer(user.id, question_1.id, 'Wow')
        db.session.add(answer_1)
        db.session.commit()
        user_serialized = user_schema.dump(user).data
        assert len(user_serialized) == 15
        assert user_serialized['stars_total_count'] == 0
        assert user_serialized['upvotes_total_count'] == 0
        assert user_serialized['downvotes_total_count'] == 0
        assert user_serialized['snippets_count'] == 2
        assert user_serialized['questions_count'] == 3
        assert user_serialized['comments_count'] == 1
        assert user_serialized['answers_count'] == 1
        assert user_serialized['id'] == 1
        assert user_serialized['username'] == 'user'
        assert user_serialized['email'] == 'user@example.com'
        assert isinstance(user_serialized['created'], str)
        assert isinstance(user_serialized['updated'], str)

    def test_serialization_with_marshmallow_and_user_information(self, db):
        user = UserFactory()
        db.session.commit()
        user_information = UserInformation(id_user=user.id, country="Canada", bio="Sadness")
        db.session.add(user_information)
        user_schema = UserSchema()
        user_serialized = user_schema.dump(user).data
        assert user_serialized['information']['country'] == "Canada"
        assert user_serialized['information']['bio'] == "Sadness"
        assert len(user_serialized['information']) == 2

    def test_serialized_with_marshmallow_with_notifications(self, db, user):
        _user = user.get()
        _user_should_ignore = UserFactory(username="Carl")
        db.session.commit()
        notification = Notification(id_user=_user.id, description="Carl answered your question")
        db.session.add(notification)
        notification = Notification(id_user=_user.id, description="Tomas answered your question",
                                    url="/questions/23")
        db.session.add(notification)
        notification = Notification(id_user=_user_should_ignore.id, description="Tomas answered your question")
        db.session.add(notification)
        db.session.commit()
        user_notification_schema = UserNotificationSchema()
        user_notification_serialized = user_notification_schema.dump(_user).data
        assert len(user_notification_serialized['notification']) == 2
        assert 'url' not in user_notification_serialized['notification'][0]
        assert 'url' in user_notification_serialized['notification'][1]
        user_notification_serialized = user_notification_schema.dump(_user_should_ignore).data
        assert len(user_notification_serialized['notification']) == 1
        assert 'url' not in user_notification_serialized['notification'][0]

    def test_serialized_with_marshmallow_with_follow_data(self, db, user):
        _user = user.get()
        user_followed_1  = UserFactory(username="user__1", email="user__1@gmail.com")
        user_followed_2  = UserFactory(username="user__2", email="user__2@gmail.com")
        user_followers_1 = UserFactory(username="user__3", email="user__3@gmail.com")
        user_followers_2 = UserFactory(username="user__4", email="user__4@gmail.com")
        user_followers_3 = UserFactory(username="user__5", email="user__5@gmail.com")
        db.session.commit()
        _user.followed.append(user_followed_1)
        _user.followed.append(user_followed_2)
        _user.followers.append(user_followers_1)
        _user.followers.append(user_followers_2)
        _user.followers.append(user_followers_3)
        user_schema = UserSchema()
        user_serialized = user_schema.dump(_user).data
        assert user_serialized['followed_count'] == 2
        assert user_serialized['followers_count'] == 3