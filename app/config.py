import os

APP_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'TODO, Enviroment Variable'


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
    SECRET_KEY = '123456'
    REDIS_URL = "redis://:@localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + APP_DIR + '/../tmp/talkcode.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"