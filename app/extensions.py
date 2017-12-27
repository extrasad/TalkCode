from flask_socketio import SocketIO
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

redis_store = FlaskRedis()
socketio    = SocketIO()
db          = SQLAlchemy()