import pytest, jwt

from flask import json

from ..factories import UserFactory
from ...app.controllers.interface.authentication.descriptions import SIGN_UP_DESCRIPTIONS, SIGN_IN_DESCRIPTIONS
from ...app.models import User


@pytest.mark.usefixtures('db', 'user', 'app')
class TestSignUpAuthentication:
  """Test signup route"""
  
  _ = '/api/auth/' # Route of API
  
  def test_signup_successfully(self, db, user, app):
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
      'email':'email@email.com',
      'password':'123456',
      'username':'charlyjazz',
    }), content_type='application/json')

    assert User.query.count() == 1
    assert 'payload' in r.data
    assert 'idToken' in r.data
    assert 'expiresIn' in r.data
    assert 'user' in r.data
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 201
    assert r.status_code == 201

    decode = jwt.decode(json.loads(r.data)['payload']['idToken'], app.config['VERIFY_KEY'], algorithms='RS256')

    assert decode['sub'] == 1

  def test_email_in_already_use(self, db, user, app):
    user = UserFactory(username='charlyjazz', email='charlyjazz@gmail.com')
    db.session.commit()
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
      'email':'charlyjazz@gmail.com',
      'password':'123456',
      'username':'charlyrock',
    }), content_type='application/json')

    assert User.query.count() == 1
    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 409
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['EMAIL_EXISTS']

  def test_username_in_already_use(self, db, user, app):
    user = UserFactory(username='charlyjazz', email='charlyjazz@gmail.com')
    db.session.commit()
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
      'email':'charlyrock@gmail.com',
      'password':'123456',
      'username':'charlyjazz',
    }), content_type='application/json')

    assert User.query.count() == 1
    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 409
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['USERNAME_EXISTS']

  def test_username_invalid_format(self, db, user, app):
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
      'email':'charlyrock@gmail.com',
      'password':'123456',
      'username':'',
    }), content_type='application/json')

    assert User.query.count() == 0
    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 400
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['INVALID_USERNAME']

  def test_password_invalid_format(self, db, user, app):
      r = app.test_client().post(self._ + 'signup', data=json.dumps({
        'email':'charlyrock@gmail.com',
        'password':'',
        'username':'charlyrock',
      }), content_type='application/json')

      assert User.query.count() == 0
      assert 'payload' not in r.data
      assert json.loads(r.data)['status'] == 400
      assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['INVALID_PASSWORD']

  def test_email_invalid_format(self, db, user, app):
      r = app.test_client().post(self._ + 'signup', data=json.dumps({
        'email':'',
        'password':'123456',
        'username':'charlyrock',
      }), content_type='application/json')

      assert User.query.count() == 0
      assert 'payload' not in r.data
      assert json.loads(r.data)['status'] == 400
      assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['INVALID_EMAIL']

  def test_username_missing_format(self, db, user, app):
      r = app.test_client().post(self._ + 'signup', data=json.dumps({
        'email':'',
        'password':'123456'
      }), content_type='application/json')

      assert User.query.count() == 0
      assert 'payload' not in r.data
      assert json.loads(r.data)['status'] == 400
      assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['MISS_USERNAME']
  
  def test_password_missing_format(self, db, user, app):
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
        'email':'',
        'username':'charlyrock',
    }), content_type='application/json')

    assert User.query.count() == 0
    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 400
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['MISS_PASSWORD']
  
  def test_email_missing_format(self, db, user, app):
    r = app.test_client().post(self._ + 'signup', data=json.dumps({
        'password':'123456',
        'username':'charlyrock',
    }), content_type='application/json')

    assert User.query.count() == 0
    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 400
    assert json.loads(r.data)['description'] == SIGN_UP_DESCRIPTIONS['MISS_EMAIL']


@pytest.mark.usefixtures('db', 'user', 'app')
class TestSignInAuthentication:
  """Test signin route"""
  
  _ = '/api/auth/' # Route of API

  def test_signin_successfully(self, db, user, app):
    user = UserFactory(username='charlyjazz', email='charlyjazz@gmail.com')
    r = app.test_client().post(self._ + 'signin', data=json.dumps({
      'email':'charlyjazz@gmail.com',
      'password':'123456'
    }), content_type='application/json')

    assert 'payload' in r.data
    assert 'idToken' in r.data
    assert 'expiresIn' in r.data
    assert 'user' in r.data
    assert json.loads(r.data)['description'] == SIGN_IN_DESCRIPTIONS['SUCCESS']
    assert json.loads(r.data)['status'] == 201
    assert r.status_code == 201

    decode = jwt.decode(json.loads(r.data)['payload']['idToken'], app.config['VERIFY_KEY'], algorithms='RS256')

    assert decode['sub'] == 1

  def test_password_not_match(self, db, user, app):
    user = UserFactory(username='charlyjazz', email='charlyjazz@gmail.com')
    r = app.test_client().post(self._ + 'signin', data=json.dumps({
      'email':'charlyjazz@gmail.com',
      'password':'123456789',
      'username':'charlyjazz',
    }), content_type='application/json')

    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 401
    assert json.loads(r.data)['description'] == SIGN_IN_DESCRIPTIONS['NOT_MATCH']

  def test_email_not_match(self, db, user, app):
    user = UserFactory(username='charlyjazz', email='charlyjazz@gmail.com')
    r = app.test_client().post(self._ + 'signin', data=json.dumps({
      'email':'charlyrock@gmail.com',
      'password':'123456789'
    }), content_type='application/json')

    assert 'payload' not in r.data
    assert json.loads(r.data)['status'] == 401
    assert json.loads(r.data)['description'] == SIGN_IN_DESCRIPTIONS['NOT_MATCH']