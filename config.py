import os

class Config(object):
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/cursoflask?charset=utf8&use_unicode=True'
    SQLALCHEMY_TRACK_MODIFICATIONS = False