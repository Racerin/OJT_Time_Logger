"""
Everythong to do with flask app database.
"""


__all__ = ["get_db", "close_db", "init_app", "get_user"]
__version__ = '0.1'
__author__ = "Darnell Baird"


import sqlite3
import click
import hashlib

import flask

import PARAM
import library
import config


# db_filename = "::memory::"
schema_file = "static/schema.sql"


#PASSWORD CONTROL
pw_salt = getattr(config, "SALT", "").encode("utf-8")


def salt_password(password) -> bytes:
    """Salts password using pbkdf2_hmac."""
    # https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256', 
        password=password.encode('utf-8'), 
        salt=pw_salt, 
        iterations=int(1e6)
        )
    return key


def is_password(password : str, salted : bytes):
    """Compare a new password to the salted value"""
    salted_password = salt_password(password)
    return salted_password == salted


#USER CONTROL
user_unique_fields = ['user_id', 'email', 'username']


def __get_user(key, field_int) -> sqlite3.Row:
    """Get sqlite row of user information 
    based on selected field and key of the field.
    """
    sql = """
    SELECT user_id, username, salt_password, email FROM Users WHERE {}=?;
    """.format(user_unique_fields)
    db = get_db()
    try:
        rows = db.execute(sql, (key,))
        for row in rows:
            return row
    except sqlite3.ProgrammingError:
        return None


def get_user(user_id : int) -> sqlite3.Row:
    """Get sqlite row of user information with user_id."""
    return __get_user(user_id, 0)


def get_user_from_email(email : str) -> sqlite3.Row:
    """Get sqlite row of user information from email or email."""
    return __get_user(email, 2)


def get_user_from_username(username : str) -> sqlite3.Row:
    """Get sqlite row of user information from email or username."""
    return __get_user(username, 2)


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in flask.g:
        flask.g.db = sqlite3.connect(PARAM.DATABASE.FILENAME)
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
    """Clear existing data and create new tables."""
    db = get_db()

    with flask.current_app.open_resource(schema_file) as f:
        db.executescript(f.read().decode("utf8"))


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
    with app.app_context():
        init_db()
    # print("DEFAULT PASSWORDS xxxxxxxxxxxxxxx")
    # print(salt_password('Bass Durag Cheese Bed M#torcycle'))
    # print(salt_password('Egg Dinosaur Wa(l Experience Keyboard'))
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)