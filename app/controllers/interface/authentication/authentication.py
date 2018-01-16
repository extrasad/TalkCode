import os, jwt, datetime

from flask import Blueprint, request, jsonify, current_app

from ....models.user import User, db
from ....schemas.authorized_payload import AuthorizedPayLoadSchema
from ....utils.get_data_or_400 import get_data_or_400
from descriptions import SIGN_UP_DESCRIPTIONS, SIGN_IN_DESCRIPTIONS


app = Blueprint('authentication', __name__)


@app.route('/api/auth/signup', methods=['POST'])
def signup():
  """
  Request Body Payload:
  email	    string  The email for the user to create.
  password  string  The password for the user to create.
  username  string  The username for the user to create.
  Response Payload:
  idToken	      string	A Auth ID token for the newly created user.
  expiresIn	    string	The number of seconds in which the ID token expires.
  user	        string	A Object with the user information
  """

  data = request.get_json()
  email    = get_data_or_400(data, 'email', SIGN_UP_DESCRIPTIONS['MISS_EMAIL'])
  password = get_data_or_400(data, 'password', SIGN_UP_DESCRIPTIONS['MISS_PASSWORD'])
  username = get_data_or_400(data, 'username', SIGN_UP_DESCRIPTIONS['MISS_USERNAME'])

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

    encode = new_resource.encode_auth_token()
    token, expiresIn = encode[0], encode[1]

    user_schema = schema.dump({
      'idToken': token,
      'expiresIn': expiresIn.isoformat(),
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


@app.route('/api/auth/signin', methods=['POST'])
def signin():
  """
  Request Body Payload:
  email	    string  The email the user is signing in with.
  password  string  The password for the account.
  Response Payload:
  idToken	      string	A Auth ID token for the newly created user.
  expiresIn	    string	The number of seconds in which the ID token expires.
  user	        string	A Object with the user information
  """

  data = request.get_json()
  email    = get_data_or_400(data, 'email', SIGN_IN_DESCRIPTIONS['MISS_EMAIL'])
  password = get_data_or_400(data, 'password', SIGN_IN_DESCRIPTIONS['MISS_PASSWORD'])

  query = db.session.query(User) \
          .filter(User.email == email) \
          .one_or_none()

  if (query != None):
    if (query.password == password):
      schema = AuthorizedPayLoadSchema()
      encode = query.encode_auth_token()
      token, expiresIn = encode[0], encode[1]

      user_schema = schema.dump({
        'idToken': token,
        'expiresIn': expiresIn.isoformat(),
        'user': query,
      })

      return jsonify({
        'status': 201,
        'description': SIGN_IN_DESCRIPTIONS['SUCCESS'],
        'payload': user_schema.data
      }), 201

    else:
      return jsonify({
        'status': 401,
        'description': SIGN_IN_DESCRIPTIONS['NOT_MATCH'],
      }), 401

  else:
    return jsonify({
        'status': 401,
        'description': SIGN_IN_DESCRIPTIONS['NOT_MATCH'],
      }), 401