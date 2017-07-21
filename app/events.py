from flask import request
from flask_security import current_user
from flask_socketio import SocketIO, emit
from flask_redis import FlaskRedis


redis_store = FlaskRedis()
socketio = SocketIO()


@socketio.on('connected')
def connected():
    redis_store.set("user-%s" % current_user.id, request.sid)

    print "%s connected" % (request.sid)
    print redis_store.get("user-%s" % current_user.id)

@socketio.on('disconnect')
def disconnect():
    redis_store.delete("user-%s" % current_user.id)

    print "%s disconnected" % (request.sid)
    print redis_store.get("user-%s" % current_user.id)

@socketio.on('send_notification')
def send_notification(message):
    print message['notification']
    print message['sid']

    emit('new_notification', message['notification'], room=message['sid'])