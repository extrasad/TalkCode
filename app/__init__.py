from flask import Flask
from extensions import db, socketio, redis_store
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    register_extensions(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    socketio.init_app(app)
    redis_store.init_app(app)

def register_blueprints(app):
    pass