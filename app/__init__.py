# coding=utf-8
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
from config import DevelopmentConfig
from models import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from admin import create_admin

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()
mysql = MySQL(app)
engine = create_engine("mysql://root@localhost/talkcode?charset=utf8&use_unicode=0")
create_admin(app)

if not database_exists(engine.url):
    create_database(engine.url)
csrf.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()
db.init_app(app)

from app import views, models, filters
