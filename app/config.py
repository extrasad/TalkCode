import os, string, random

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'TODO, Enviroment Variable'

class DevelopmentConfig(Config):
    SECRET_KEY = '123456'
    DEBUG = True
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + basedir  + '/../tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True