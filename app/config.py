import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.realpath(os.path.join(basedir, "../.env")))


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", "sqlite:///../instance/dev.sqlite")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_ROUTE = os.getenv("ADMIN_ROUTE", "/admin")

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

    LDAP_OPENLDAP = os.getenv("LDAP_OPENLDAP").lower() in ['1', 'true']
    LDAP_SCHEMA = os.getenv("LDAP_SCHEMA")
    LDAP_HOST = os.getenv("LDAP_HOST")
    LDAP_PORT = os.getenv("LDAP_PORT")
    LDAP_USERNAME = os.getenv("LDAP_USERNAME")
    LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
    LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
    LDAP_GROUPS_OBJECT_FILTER = os.getenv("LDAP_GROUPS_OBJECT_FILTER")
    LDAP_GROUP_OBJECT_FILTER = os.getenv("LDAP_GROUP_OBJECT_FILTER")
    LDAP_USER_OBJECT_FILTER = os.getenv("LDAP_ADMIN_USER_FILTER")
    LDAP_GROUP_MEMBER_FILTER = os.getenv('LDAP_GROUP_MEMBER_FILTER')
    LDAP_GROUP_MEMBER_FILTER_FIELD = os.getenv('LDAP_GROUP_MEMBER_FILTER_FIELD')
    LDAP_LOGIN_VIEW = 'admin.login'


class TestingConfig(ProdConfig):
    ALLOW_DEV_COMMANDS = True
