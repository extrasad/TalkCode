# coding=utf-8
from datetime import date
from views import app, MySQL
from flask_wtf import CsrfProtect
from config import DevelopmentConfig
from models import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()
mysql = MySQL(app)
engine = create_engine("mysql://root@localhost/cursoflask?charset=utf8&use_unicode=0")


def run_app():
    if not database_exists(engine.url):
        create_database(engine.url)
    """"Run app web"""
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    db.init_app(app)
    app.run(port=8000, debug=True)
    return None

