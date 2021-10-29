from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simpleldap import LDAP

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
ldap = LDAP()
