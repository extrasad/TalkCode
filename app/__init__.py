from flask import Flask
from extensions import db, socketio, redis_store
from config import DevelopmentConfig
from models import *
from commands import test


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    with app.app_context():
        db.create_all()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    socketio.init_app(app)
    redis_store.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    pass


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(test)