from flask_socketio import SocketIO
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


redis_store = FlaskRedis()
socketio    = SocketIO()
db          = SQLAlchemy()
marshmallow = Marshmallow()