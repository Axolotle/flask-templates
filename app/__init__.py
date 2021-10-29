import os

from flask import Flask, g, session

from app import client, admin
from app.extensions import db, migrate, ldap
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
    ldap.init_app(app)

    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            # This is where you'd query your database to get the user info.
            g.user = {}
            # Create a global with the LDAP groups the user is a member of.
            g.ldap_groups = ldap.get_user_groups(user=session['user_id'])


def register_commands(app):
    app.cli.add_command(admin_cli)


def register_blueprints(app):
    app.register_blueprint(client.routes.bp)
    app.register_blueprint(admin.routes.bp, url_prefix=app.config['ADMIN_ROUTE'])

    if (app.config["ENV"] == 'development'):
        # allow werkzeug to serve static files from instance_path in dev mode
        with app.app_context():
            from app import uploads
            app.register_blueprint(uploads.bp, url_prefix='/uploads')
    else:
        # allow using `url_for('uploads.static', filename="file.jpg")` without registering any blueprints
        app.add_url_rule("/uploads/<filename>",
                         endpoint="uploads.static", build_only=True)
