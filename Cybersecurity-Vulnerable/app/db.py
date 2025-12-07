import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    Get database connection.
    Creates a new connection if one doesn't exist for the current request.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Return rows as dict-like objects

    return g.db


def close_db(e=None):
    """
    Close database connection at the end of request.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database using schema.sql file.
    Clear existing data and create fresh tables.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    CLI command to initialize the database.
    Usage: flask init-db
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Register database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)