import os, string, random

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/talkcode?charset=utf8&use_unicode=0'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'talkcode'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    WTF_CSRF_ENABLED = True
    POSTS_PER_PAGE = 3
    ASSETS_DEBUG = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
