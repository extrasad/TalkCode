import os

from flask import Blueprint, request, jsonify

from ....models.user import User, AuthorizedPayLoadSchema, db
from descriptions import SIGN_UP_DESCRIPTIONS

app = Blueprint('authentication', __name__)


@app.route('/api/auth/signup', methods=['POST'])
def signup():
  """
  Resquest Body Payload:
  email	    string  The email for the user to create.
  password  string  The password for the user to create.
  Response Payload:
  idToken	      string	A Firebase Auth ID token for the newly created user.
  email	        string	The email for the newly created user.
  refreshToken	string	A Firebase Auth refresh token for the newly created user.
  expiresIn	    string	The number of seconds in which the ID token expires.
  """

  data = request.get_json()
  email = data['email']
  password = data['password']
  username = data['username']

  # Search User by email or username
  query = db.session.query(User) \
          .filter((User.email == email) | (User.username == username)) \
          .one_or_none()

  if (query == None):

    try:
      new_resource = User(username, email, password)
    except ValueError as error: # Model Validation
      return jsonify({
        'status': 400,
        'description': str(error),
      }), 400

    db.session.add(new_resource)
    db.session.commit()
    schema = AuthorizedPayLoadSchema()

    user_schema = schema.dump({
      'idToken': '123456789',
      'refreshToken': '123456789',
      'expiresIn': '3600',
      'user': new_resource,
    })

    return jsonify({
      'status': 201,
      'description': SIGN_UP_DESCRIPTIONS['SUCCESS'],
      'payload': user_schema.data
    }), 201

  else:
    description = SIGN_UP_DESCRIPTIONS['USERNAME_EXISTS'] \
                  if query.username == username else \
                  SIGN_UP_DESCRIPTIONS['EMAIL_EXISTS']

    return jsonify({
      'status': 409,
      'description': description,
    }), 409