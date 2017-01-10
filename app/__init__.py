# coding=utf-8
from flask import Flask, url_for
from flask_wtf import CsrfProtect
from flask_assets import Environment
from flask_security import SQLAlchemyUserDatastore, Security
from config import DevelopmentConfig
from assets import create_assets
from models import *
from form import SecurityRegisterForm
from admin import MyFileAdmin, _Admin, create_security_admin

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import os.path

path = os.path.join(os.path.dirname(__file__), 'static')

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()
assets = Environment(app)
create_assets(assets)

engine = create_engine("mysql://root@localhost/talkcode?charset=utf8&use_unicode=0")
if not database_exists(engine.url):
    create_database(engine.url)

db.init_app(app)
csrf.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    register_form=SecurityRegisterForm)

create_security_admin(app=app, path=path)

with app.app_context():
    db.create_all()

from app import views, models, filters, assets, admin