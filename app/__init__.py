# coding=utf-8
from flask import Flask, redirect, url_for, request
from flask_wtf import CSRFProtect
from flask_assets import Environment
from flask_security import SQLAlchemyUserDatastore, Security, utils as security_utils
from flask_redis import FlaskRedis

from config import DevelopmentConfig
from assets import create_assets
from form import SecurityRegisterForm
from admin import create_security_admin
from models import *
from filters import superwordwrap
from events import socketio, redis_store

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import os.path

path = os.path.join(os.path.dirname(__file__), 'static')

user_datastore = None


def create_app():

    global user_datastore

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    csrf = CSRFProtect()
    assets = Environment(app)
    create_assets(assets)
    redis_store.init_app(app)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    db.init_app(app)
    csrf.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore, register_form=SecurityRegisterForm)
    create_security_admin(app=app, path=path)

    from views import app as application
    app.register_blueprint(application)

    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    @app.before_first_request
    def before_first_request():
        # Create the Roles "admin" and "end-user" -- unless they already exist
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='end-user', description='End user')

        # Create two Users for testing purposes -- unless they already exists.
        encrypted_password = security_utils.encrypt_password('password')
        if not user_datastore.get_user('someone@example.com'):
            user_datastore.create_user(username='kathorq',
                                       password=encrypted_password,
                                       email='someone@example.com')
        if not user_datastore.get_user('admin@example.com'):
            user_datastore.create_user(username='carlosjazz',
                                       password=encrypted_password,
                                       email='admin@example.com')

        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
        # Users already have these Roles.) Again, commit any database changes.
        user_datastore.add_role_to_user('someone@example.com', 'end-user')
        user_datastore.add_role_to_user('admin@example.com', 'admin')
        db.session.commit()


    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('main.index')), 404  # No found

    app.add_template_filter(superwordwrap)

    return app