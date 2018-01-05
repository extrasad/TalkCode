from flask import Flask
from extensions import *
from config import DevelopmentConfig, STATIC_FOLDER
from models import *
from commands import test

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def create_app(config=DevelopmentConfig):
    app = Flask(__name__, static_folder = STATIC_FOLDER)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    with app.app_context():
        db.create_all()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    socketio.init_app(app)
    redis_store.init_app(app)
    marshmallow.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    from .controllers.web.web import app as application
    app.register_blueprint(application)
    from .controllers.interface.authentication.authentication import app as namespace
    app.register_blueprint(namespace)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(test)