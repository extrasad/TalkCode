import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
