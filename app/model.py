"""Script containing other classes used in app.
I think it suppose to have SQLAlchemy in here. 
https://medium.com/analytics-vidhya/how-to-test-flask-applications-aef12ae5181c

"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["User"]


import dataclasses
import sqlite3
import functools

import flask
import flask_login

from . import db as DB
import library


@dataclasses.dataclass
class User(flask_login.UserMixin):

    user_id : int = None
    username : str = ""
    password : str = dataclasses.field(default="", repr=False)   # Never stored.
    salt_password : bytes = dataclasses.field(default=b'', repr=False)
    email : str = ""
    is_admin : bool = False
    # https://flask-login.readthedocs.io/en/latest/#your-user-class
    is_active : bool = True

    def get_id(self):
        return self.DB.get_user_from_email(self.email).user_id

    def __post_init__(self):
        # Ensure password is salted
        if self.password and isinstance(self.password, str):
            self.salt_password = DB.salt_password(self.password)
        # Assign password property
        self.password = property(
            # lambda: raise ValueError("Cannot access user password."),
            lambda: None,
            lambda pw: setattr(self, "salt_password", DB.salt_password(pw)),
            lambda: delattr(self, 'salt_password'),
            )

    @classmethod
    def from_register_form(cls, form) -> 'User':
        """Create user from UserRegistrationForm"""
        data = form.data
        usr = User(
            username=data['username'],
            password=data['password1'],
            email=data['email'],
            )
        return usr

    @classmethod
    def from_row(cls, row) -> 'User':
        """Creates a user from a database row object."""
        usr = User(
            user_id=row['user_id'],
            username=row['username'],
            salt_password=row['salt_password'],
            email=row['email'],
            is_admin=bool(row['is_admin']),
            )
        return usr

    @classmethod
    def admin_access(cls, func):
        """Wrapper function for granting access if is admin."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            usr = flask_login.current_user()
            if usr.is_admin:
                return func(*args, **kwargs)
            else:
                return "Unauthorized Access."
        return wrapper

    def __eq__(self, other):
        """Compare none property attributes."""
        for k,v in vars(self).items():
            # Ignore functions and property values
            if callable(v) or isinstance(v, property): continue
            try:
                if v != getattr(other, k):
                    return False
            except ValueError:
                return False
        return True


    class DB:

        _user_unique_fields = ['user_id', 'email', 'username', 'is_admin']
 
        @classmethod
        def get_db(cls) -> sqlite3.Connection:
            db = DB.get_db()
            return db

        @classmethod
        def __get_user(cls, key, field_int) -> 'User':
            """Get user based on selected field and key of the field."""
            user_field = cls._user_unique_fields[field_int]
            sql = """
            SELECT user_id, username, salt_password, email, is_admin FROM Users WHERE {}=? AND is_active=1 LIMIT 1;
            """.format(user_field)
            db = cls.get_db()
            try:
                rows = db.execute(sql, (key,))
                for row in rows:
                    return User.from_row(row)
            except sqlite3.ProgrammingError:
                flask.flash(f"There was an error in retrieving the user via '{user_field}'.")
                return None

        @classmethod
        def get_user_from_id(cls, user_id : int) -> 'User':
            """Get user from user_id."""
            return cls.__get_user(user_id, 0)

        @classmethod
        def get_user_from_email(cls, email : str) -> 'User':
            """Get user from email."""
            return cls.__get_user(email, 1)

        @classmethod
        def get_user_from_username(cls, username : str) -> 'User':
            """Get user from username."""
            return cls.__get_user(username, 2)

        @classmethod
        def get_user_from_username_email(cls, username_email : str) -> 'User':
            """Get user from email, else username"""
            row = cls.get_user_from_email(username_email)
            if row is None:
                row = cls.get_user_from_username(username_email)
            return row

        @classmethod
        def _exists(cls, val, field_int) -> bool:
            """Determine whether val of Users'
            field of 'field_int' exists.
            """
            attr = cls._user_unique_fields[field_int]
            sql = f"SELECT {attr} FROM Users WHERE {attr}=? LIMIT 1;"
            db = cls.get_db()
            rows = db.execute(sql, (val,))
            for row in rows:
                return val == row[attr]     #redundant
 
        @classmethod
        def email_exists(cls, email : str) -> bool:
            """Confirms whether email exists."""
            return cls._exists(email, 1)
            sql = "SELECT email FROM Users WHERE email==? LIMIT 1;"
            db = cls.get_db()
            rows = db.execute(sql, (email,))
            for row in rows:
                return email == row['email']

        @classmethod
        def login(cls, username_email : str, password : str) -> sqlite3.Row:
            """Returns valid user if username and password matches, else no user information.
            """
            usr = cls.get_user_from_username_email(username_email)
            if usr:
                if DB.salt_password(password) == usr.salt_password:
                    return usr
            return None

        @classmethod
        def insert_user(cls, user : 'User', commit=True):
            """Submits user to the database."""
            db = cls.get_db()
            sql2 = """INSERT INTO Users (
                username, salt_password, email, is_admin, is_active
                )
                VALUES(:username,:salt_password,:email,:is_admin,:is_active);"""
            values = vars(user)
            db.execute(sql2, values)
            if commit:
                db.commit()
            else:
                return db

        @classmethod
        def add_example_users(cls):
            """Add test users."""
            users = [
                User(
                    username='FooBar',
                    password='goatmilk',
                    email='example@example.com',
                ),
            ]
            for usr in users:
                conn = cls.insert_user(usr, commit=False)
            conn.commit()

        @classmethod
        def _change_attribute(cls, atrbt, user_id, new_value) -> bool:
            """Change attribute  of user with user_id to value 'new_value'.
            Contains magic for password.
            Untested.
            """
            # Salt the password. 'password' filter magic.
            if atrbt.strip() == 'password':
                new_value = DB.salt_password(new_value)
                atrbt = 'salt_password'
            sql = f"""
            UPDATE Users
            SET {atrbt} = ?
            WHERE user_id = ?
            LIMIT 1;"""
            values = (new_value, user_id)
            db = cls.get_db()
            try:
                db.execute(sql, values)
                db.commit()
            except sqlite3.Error as err:
                flask.current_app.logger.error(f"This is the sqlite error:\n {err}")
                return False
            return True

        @classmethod
        def change_username(cls, user_id : int, new_username : str) -> bool:
            """Change username to 'new_username' of user with user_id 'user_id'.
            """
            return cls._change_attribute('username', user_id, new_username)

        @classmethod
        def change_email(cls, user_id : int, new_email : str) -> bool:
            """Change email to 'new_email' of user with user_id 'user_id'."""
            return cls._change_attribute('email', user_id, new_email)

        @classmethod
        def change_password(cls, user_id : int, new_password : str) -> bool:
            """Change password to 'new_password' of user with user_id 'user_id'.
            """
            return cls._change_attribute('password', user_id, new_password)

        @classmethod
        def clear_users(cls, delete_admin=False):
            if delete_admin:
                sql = "DELETE FROM Users;"
            else:
                sql = "DELETE FROM Users WHERE is_admin=0;"
            db = cls.get_db()
            db.execute(sql)
            db.commit()
        