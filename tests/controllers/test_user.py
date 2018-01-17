import pytest, jwt

from flask import json

from ..factories import UserFactory
from ...app.models import User, Notification, Question, Answer, Snippet
from ...app.controllers.interface.user.descriptions import GET_USER_DESCRIPTIONS, GET_USER_NOTIFICATIONS_DESCRIPTIONS, GET_USER_QUESTIONS_DESCRIPTIONS, \
GET_USER_ANSWERS_DESCRIPTIONS, GET_USER_SNIPPETS_DESCRIPTIONS


@pytest.mark.usefixtures('db', 'user', 'app')
class TestGetUser:
  """ Test GetUser route"""

  _ = 'api/users/'

  def test_get_user_successfully(self, db, user, app):
    user = UserFactory()
    db.session.commit()
    r = app.test_client().get(self._ + str(user.id))

    assert r.status_code == 200
    assert 'payload' in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 200
  
  def test_get_user_not_found(self, db, user, app):
    r = app.test_client().get(self._ + '1')
    
    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_DESCRIPTIONS['NOT_FOUND']
    assert json.loads(r.data)['status'] == 404


@pytest.mark.usefixtures('db', 'user', 'app')
class TestGetUserNotifications:
  """ Test GetUserNotifications route"""

  _ = 'api/users/'

  def test_get_user_notifications(self, db, user, app):
    user = UserFactory()
    db.session.commit()
    notification_1 = Notification(id_user=user.id, 
                                  description="Carl answered your question",
                                  url="/questions/1")
    notification_2 = Notification(id_user=user.id,
                                  description="Max answered your question",
                                  url="/questions/1")
    db.session.add(notification_1)
    db.session.add(notification_2)
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/notifications')

    assert r.status_code == 200
    assert len(json.loads(r.data)['payload']['notification']) == 2
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_NOTIFICATIONS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 200
  
  def test_get_user_notifications_with_incorrect_user_id(self, db, user, app):
    id = 1
    
    r = app.test_client().get(self._ + str(id) + '/notifications')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == 'The resource {} with the id: {}'.format(User.__tablename__, id)
    assert json.loads(r.data)['status'] == 404
  
  def test_get_user_notifications_without_notifications(self, db, user, app):
    user = UserFactory()
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/notifications')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] != GET_USER_NOTIFICATIONS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['description'] == GET_USER_NOTIFICATIONS_DESCRIPTIONS['NOT_FOUND']
    assert json.loads(r.data)['status'] == 404

@pytest.mark.usefixtures('db', 'user', 'app')
class TestGetUserQuestions:
  """ Test GetUserQuestions route"""

  _ = 'api/users/'

  def test_get_user_questions(self, db, user, app):
    user = UserFactory()
    db.session.commit()
    question_1 = Question(id_user=user.id, text="What is the life?")
    question_2 = Question(id_user=user.id, text="What is existence?")
    db.session.add(question_1)
    db.session.add(question_2)
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/questions')

    assert r.status_code == 200
    assert len(json.loads(r.data)['payload']['questions']) == 2
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_QUESTIONS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 200
  
  def test_get_user_questions_with_incorrect_user_id(self, db, user, app):
    id = 1
    
    r = app.test_client().get(self._ + str(id) + '/questions')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == 'The resource {} with the id: {}'.format(User.__tablename__, id)
    assert json.loads(r.data)['status'] == 404

  def test_get_user_questions_without_questions(self, db, user, app):
    user = UserFactory()
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/questions')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] != GET_USER_QUESTIONS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['description'] == GET_USER_QUESTIONS_DESCRIPTIONS['NOT_FOUND']
    assert json.loads(r.data)['status'] == 404


@pytest.mark.usefixtures('db', 'user', 'app')
class TestGetUserAnswers:
  """ Test GetUserAnswers route"""

  _ = 'api/users/'

  def test_get_user_answers(self, db, user, app):
    user_question = UserFactory()
    user_anwswer = UserFactory(username='Rivasan', email='rivasan@gmail.com')
    db.session.commit()
    question = Question(id_user=user_question.id, text="What is the life?")
    db.session.add(question)
    db.session.commit()
    answer = Answer(user_anwswer.id, question.id, "Answer?")
    db.session.add(answer)
    db.session.commit()

    r = app.test_client().get(self._ + str(user_anwswer.id) + '/answers')

    assert r.status_code == 200
    assert len(json.loads(r.data)['payload']['answers']) == 1
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_ANSWERS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 200
  
  def test_get_user_answers_with_incorrect_user_id(self, db, user, app):
    id = 1
    
    r = app.test_client().get(self._ + str(id) + '/answers')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == 'The resource {} with the id: {}'.format(User.__tablename__, id)
    assert json.loads(r.data)['status'] == 404

  def test_get_user_answers_without_answers(self, db, user, app):
    user = UserFactory()
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/answers')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] != GET_USER_ANSWERS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['description'] == GET_USER_ANSWERS_DESCRIPTIONS['NOT_FOUND']
    assert json.loads(r.data)['status'] == 404


@pytest.mark.usefixtures('db', 'user', 'app')
class TestGetUserSnippets:
  """ Test GetUserSnippets route"""

  _ = 'api/users/'

  def test_get_user_snippets(self, db, user, app):
    user = UserFactory()
    db.session.commit()

    snippet = Snippet(id_user=user.id, filename="application.rb",
                      body="lorem ipsum", description="lorem ipsum")
    db.session.add(snippet)
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/snippets')

    assert r.status_code == 200
    assert len(json.loads(r.data)['payload']['snippets']) == 1
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == GET_USER_SNIPPETS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 200
  
  def test_get_user_snippets_with_incorrect_user_id(self, db, user, app):
    id = 1
    
    r = app.test_client().get(self._ + str(id) + '/snippets')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] == 'The resource {} with the id: {}'.format(User.__tablename__, id)
    assert json.loads(r.data)['status'] == 404

  def test_get_user_snippets_without_snippets(self, db, user, app):
    user = UserFactory()
    db.session.commit()

    r = app.test_client().get(self._ + str(user.id) + '/snippets')

    assert r.status_code == 404
    assert 'payload' not in r.data
    assert 'description' in r.data
    assert 'status' in r.data
    assert json.loads(r.data)['description'] != GET_USER_SNIPPETS_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['description'] == GET_USER_SNIPPETS_DESCRIPTIONS['NOT_FOUND']
    assert json.loads(r.data)['status'] == 404        
