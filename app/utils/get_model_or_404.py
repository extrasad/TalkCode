from flask import jsonify, make_response, abort
from sqlalchemy.orm.exc import NoResultFound 


def get_model_or_404(model, id):
  """
  Try get one record or return abort 404
  """
  try:
    return model.query.filter_by(id=id).one()
  except NoResultFound:
    abort(make_response(jsonify({
        'status': 404,
        'description': 'The resource {} with the id: {}'.format(model.__tablename__, id)
      }), 404))