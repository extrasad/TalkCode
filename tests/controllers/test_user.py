import pytest, jwt

from flask import json

from ..factories import UserFactory
from ...app.models import User
from ...app.controllers.interface.user.descriptions import GET_USER_DESCRIPTIONS


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