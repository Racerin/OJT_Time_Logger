"""
Everythong to do with flask app database.
"""


__all__ = ["get_db", "close_db", "init_app"]
__version__ = '0.1'
__author__ = "Darnell Baird"


import sqlite3, click
import flask
from . import PARAM


# db_filename = "::memory::"
schema_file = "schema.sql"


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        flask.g.db = sqlite3.connect(PARAM.DATABASE.FILENAME)
        flask.g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = flask.g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with flask.current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# @click.command("init-db")
# @flask.with_appcontext
# def init_db_command():
#     """Clear existing data and create new tables."""
#     init_db()
#     click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)