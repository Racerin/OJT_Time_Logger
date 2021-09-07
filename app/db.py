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


# db_filename = "::memory::"
schema_file = "static/schema.sql"


#USER CONTROL
user_unique_fields = ['user_id', 'email', 'username']


def __get_user(key, field_int) -> sqlite3.Row:
    """Get sqlite row of user information 
    based on selected field and key of the field.
    """
    user_field = user_unique_fields[field_int]
    sql = """
    SELECT user_id, username, salt_password, email, is_admin FROM Users WHERE {}=? AND is_active=1;
    """.format(user_field)
    db = get_db()
    try:
        rows = db.execute(sql, (key,))
        for row in rows:
            return row
    except sqlite3.ProgrammingError:
        flask.flask(f"There was an error in retrieving the user via '{user_field}'.")
        return None


def get_user_from_email(email : str) -> sqlite3.Row:
    """Get sqlite row of user information from email or email."""
    return __get_user(email, 1)


def get_user_from_username(username : str) -> sqlite3.Row:
    """Get sqlite row of user information from email or username."""
    return __get_user(username, 2)


def get_user_from_username_email(username_email : str) -> sqlite3.Row:
    """Get sqlite row of user information from email, else username"""
    row = get_user_from_email(username_email)
    if row is None:
        row = get_user_from_username(username_email)
    return row


def email_exists(email : str) -> bool:
    """Confirms whether email exists."""
    sql = "SELECT email FROM Users email WHERE email==? LIMIT 1;"
    db = get_db()
    rows = db.execute(sql, (email,))
    for row in rows:
        return email == row['email']


def login(username_email : str, password : str) -> sqlite3.Row:
    """Returns valid user if username and password matches, else no user information.
    """
    row = get_user_from_username_email(username_email)
    if row:
        if library.is_password(password, row['salt_password']):
            return row
    return None


def insert_user(user : 'User'):
    """Submits user to the database."""
    db = get_db()
    sql2 = """INSERT INTO Users (
        username, salt_password, email, is_admin, is_active
        )VALUES(:username,:salt_password,:email,:is_admin,:is_active);"""
    values = vars(user)
    db.execute(sql2, values)
    db.commit()


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
    """Clear existing data, create new tables, and add admin and dumby user."""
    db = get_db()

    #Create Tables
    sqls = [
        "DROP TABLE IF EXISTS Users",

        "DROP TABLE IF EXISTS Clock",

        "PRAGMA foreign_keys = ON;",

        """CREATE TABLE Users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            salt_password BLOB NOT NULL,
            email TEXT UNIQUE,
            is_admin INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1
            ); """, 

        """CREATE TABLE Clock (
            user_id,
            clock_in TEXT NOT NULL,
            clock_out TEXT,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
            );""",
    ]
    for sql in sqls:
        db.execute(sql)
    #Add users
    users = [
        ('admin', b'\xda1Y[D\xa3Yg"\x0f\xd3\x1b\x83\xd7R\xe80o\xb2\xeeu;7\xe3\xd6\xfd%\x0b4~x\x92', 'drsbaird@yahoo.com', 1),
        ('FooBar', b'\x86\x98\xc8/=\x121\xd0\xf5E\xf0\x1b\xba\x17\xec\xe5\x0eG\xd3\x11\xc5O\xef\xf7\xbe\xd3\xa5\x80\x10\x85\xe6^', 'example@example.com', 0),
    ]
    sql = "INSERT INTO Users (username, salt_password, email, is_admin) VALUES(?,?,?,?);"
    db.executemany(sql, users)
    db.commit()


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