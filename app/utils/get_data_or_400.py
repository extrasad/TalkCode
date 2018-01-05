from flask import jsonify, make_response, abort

def get_data_or_400(data, key, description):
  try:
    return data[key]
  except KeyError:
    abort(make_response(jsonify({ # AMAZING FUCKING CODE, THAT SHIT HARD
        'status': 400,
        'description': description
      }), 400))