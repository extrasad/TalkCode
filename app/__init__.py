# coding=utf-8
from flask import Flask, url_for
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
from flask_assets import Environment
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.fileadmin import FileAdmin

from config import DevelopmentConfig
from assets import create_assets
from models import *
from admin import _Admin

from sqlalchemy import create_engine, or_
from sqlalchemy_utils import database_exists, create_database

import os.path


app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

csrf = CsrfProtect()

assets = Environment(app)

create_assets(assets)

mysql = MySQL(app)

engine = create_engine("mysql://root@localhost/talkcode?charset=utf8&use_unicode=0")

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore)

admin = _Admin(app, name='talkcode', template_mode='bootstrap3')

admin.add_model_views([
    User, Role, Personal_User, Curriculum_User,
    Skill, Question, TagQuestion,
    AnswerLong, Snippet, TagSnippet, Star,
    CommentSnippet, Upvote, Downvote,
    Answer_Downvote, Answer_Upvote
])

path = os.path.join(os.path.dirname(__file__), 'static')

admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

if not database_exists(engine.url):
    create_database(engine.url)
    
csrf.init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    query =  db.session.query(Role).filter(or_(Role.name=='user', Role.name=='superuser'))
    try:
        if query[0] == 'user':
            pass
    except IndexError:
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()    


from app import views, models, filters, assets, admin