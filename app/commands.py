import click
from flask.cli import AppGroup

from app.extensions import db

admin_cli = AppGroup('admin')


@admin_cli.command('db-init')
def init_db(**kwargs):
    db.create_all()
    click.echo('Database is initialized !')
