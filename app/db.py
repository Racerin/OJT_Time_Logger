"""
Everythong to do with flask app database.
"""


__all__ = ["get_db", "close_db", "init_app", "get_user"]
__version__ = '0.1'
__author__ = "Darnell Baird"


import sqlite3
import click

import flask

import PARAM
import library


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in flask.g:
        database_filename = flask.current_app.config["DATABASE"]
        flask.g.db = sqlite3.connect(database_filename)
        flask.g.db.row_factory = sqlite3.Row
    return flask.g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = flask.g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data, create new tables, and add admin and dumby user."""
    db = get_db()

    #Create Tables
    sqls = [
        "DROP TABLE IF EXISTS Clock",

        "PRAGMA foreign_keys = ON;",

        """CREATE TABLE Clocking (
            user_id,
            clock_in TEXT NOT NULL,
            clock_out TEXT,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
            );""",
    ]
    for sql in sqls:
        db.execute(sql)
    db.commit() #idk if needed


@click.command("init-db")
@flask.cli.with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)