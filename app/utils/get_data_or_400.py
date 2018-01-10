from flask import jsonify, make_response, abort

def get_data_or_400(data, key, description):
  """Try get data in request content-type application/json"""
  try:
    return data[key]
  except KeyError:
    abort(make_response(jsonify({
        'status': 400,
        'description': description
      }), 400))