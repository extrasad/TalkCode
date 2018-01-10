from flask import Blueprint, request, jsonify, current_app

from ....models.user import User, UserSchema

from descriptions import GET_USER_DESCRIPTIONS

app = Blueprint('user', __name__)


@app.route('/api/users/<int:id>')
def get_user(id):
  query = User.query.filter_by(id=id).one_or_none()
  if (query is not None):
    schema = UserSchema()
    user_serialized = schema.dump(query)
    
    return jsonify({
      'status': 200,
      'description': GET_USER_DESCRIPTIONS['SUCCESS'],
      'payload': user_serialized.data
    }), 200

  else:
    return jsonify({
    'status' : 404,
    'description': GET_USER_DESCRIPTIONS['NOT_FOUND']   
  }), 404

