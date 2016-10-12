# coding=utf-8
from datetime import date
from views import app, MySQL
from flask_wtf import CsrfProtect
from config import DevelopmentConfig
from models import db

app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect()
mysql = MySQL(app)



def run_app():
    """"Run app web"""
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    db.init_app(app)
    app.run(port=8000, debug=True)
    return None

run_app()