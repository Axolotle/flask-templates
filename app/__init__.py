import os

from flask import Flask

from app import client, admin
from app.extensions import db, migrate
from app.commands import admin_cli


def create_app(config_name='app.config.DevConfig', instance_path=None):
    app = Flask(__name__, instance_path=instance_path)

    app.config.from_object(config_name)

    # ensure the instance folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass

    register_extensions(app)
    register_commands(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)


def register_commands(app):
    app.cli.add_command(admin_cli)


def register_blueprints(app):
    app.register_blueprint(client.routes.bp)
    app.register_blueprint(admin.routes.bp, url_prefix=app.config['ADMIN_ROUTE'])

    # allow werkzeug to serve static files from instance_path in dev mode
    if (app.config["ENV"] == 'development'):
        with app.app_context():
            from app import uploads
            app.register_blueprint(uploads.bp, url_prefix='/uploads')
