import os
from utils.rsa_key import get_signing_key, get_verify_key

APP_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join('../', 'application/build')


class Config(object):
    REDIS_URL = os.environ['REDIS_URL']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']
    PASSWORD_SCHEMES = 'pbkdf2_sha512'
    STATIC_FOLDER = STATIC_FOLDER
    SIGNING_KEY = get_signing_key()
    VERIFY_KEY = get_verify_key()


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''  # TODO: CHANGE TO POSTGRES URI
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevelopmentConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """Test configuration."""

    APP_VERSION = '0.0.1'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False