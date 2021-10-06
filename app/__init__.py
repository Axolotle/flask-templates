import os

from flask import Flask

from app import base, admin
from app.extensions import db
from app.commands import admin_cli


def create_app(config_name='app.config.ProdConfig'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_name)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_extensions(app)
    register_commands(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    app.cli.add_command(admin_cli)


def register_blueprints(app):
    app.register_blueprint(base.routes.bp)
    app.register_blueprint(admin.routes.bp, url_prefix=app.config['ADMIN_ROUTE'])
