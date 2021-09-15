"""
Everythong to do with flask app database.
"""


__all__ = ["get_db", "close_db", "init_app", "get_user"]
__version__ = '0.1'
__author__ = "Darnell Baird"


import os
import click
import datetime

import flask

import PARAM
import library


#DATETIME: ISO8601


def salt_password(pw, iterations) -> bytes:
    """Salt password according to settings in library and config."""
    return library.salt_password(
        pw, 
        flask.current_app.config['SALT'], 
        iterations=PARAM.CONSTANTS.SALT_ITERATIONS,
        )


def clock_in(user_id):
    """Register an user's clock-in time."""
    sql = "INSERT INTO Clocking (user_id, clock_in) VALUES(?,?);"
    now = datetime.datetime.now().isoformat()
    db = get_db()
    db.execute(sql, (user_id, now,))
    db.commit()


def is_clocked_in(user_id) -> bool:
    """Determine whether user is clocked in."""
    sql = "SELECT clock_out FROM Clocking WHERE user_id = ? ORDER BY clock_in DESC LIMIT 1;"
    db = get_db()
    rows = db.execute(sql, (user_id,))
    for row in rows:
        if row['clock_out'] is None:
            return True 
    return False


def clock_out(user_id):
    """Clock-out user given they were clocked in."""
    sql = """UPDATE Clocking 
    SET clock_out = ?
    WHERE clock_out IS NULL AND user_id = ?
    ORDER BY clock_in DESC
    LIMIT 1;
    """
    now = datetime.datetime.now()
    db = get_db()
    db.execute(sql, (now, user_id,))
    db.commit()


def last_clock_in(user_id) -> datetime.datetime:
    """Return the time the user was last clocked in."""
    sql = """SELECT clock_in FROM Clocking 
    WHERE user_id = ? 
    ORDER BY clock_in DESC LIMIT 1;
    """
    rows = get_db().execute(sql, (user_id,))
    print('last_clock_in')
    for row in rows:
        print(row['clock_in'])
        return datetime.datetime.fromisoformat(row['clock_in'])
    return None


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in flask.g:
        database_filename = flask.current_app.config["DATABASE"]
        flask.g.db = library.get_db(database_filename)
    return flask.g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = flask.g.pop("db", None)

    if db is not None:
        db.close()


def query_db(query : str, args=(), one=False):
    """
    Execute the 'query' arg in sqlite connection with arguments 'args'.
    https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/#easy-querying
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    """Clear existing data, create new tables, and add admin and dumby user.
    https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/#initial-schemas
    'flaskr' github Rendition.
    """
    db = get_db()
    with flask.current_app.open_resource("schema.sql") as f:
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
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)