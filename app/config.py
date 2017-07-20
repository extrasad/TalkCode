import os, string, random

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class DevelopmentConfig(Config):
    SECRET_KEY = '123456'
    DEBUG = True
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/talkcode?charset=utf8&use_unicode=0'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'talkcode'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_CONNECT_TIMEOUT = 10
    MYSQL_UNIX_SOCKET = None
    MYSQL_READ_DEFAULT_FILE = None
    MYSQL_CHARSET = "utf8"
    MYSQL_USE_UNICODE = True
    MYSQL_SQL_MODE = None
    MYSQL_CURSORCLASS = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    WTF_CSRF_ENABLED = True
    POSTS_PER_PAGE = 3
    ASSETS_DEBUG = False
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_LOGIN_URL = '/login/'
    SECURITY_LOGOUT_URL = '/logout/'
    SECURITY_REGISTER_URL = '/register/'
    SECURITY_POST_LOGIN_VIEW = "/"
    SECURITY_POST_LOGOUT_VIEW = "/"
    SECURITY_POST_REGISTER_VIEW = "/"
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register.html'