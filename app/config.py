import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.realpath(os.path.join(basedir, '../.env')))



class Config:
    ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:///../instance/dev.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_ROUTE = os.getenv('ADMIN_ROUTE', '/admin')

    ALLOW_DEV_COMMANDS = False


class DevConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    ALLOW_DEV_COMMANDS = True


class ProdConfig(Config):
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class TestingConfig(ProdConfig):
    ALLOW_DEV_COMMANDS = True
