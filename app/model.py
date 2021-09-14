"""Script containing other classes used in app.
I think it suppose to have SQLAlchemy in here. 
https://medium.com/analytics-vidhya/how-to-test-flask-applications-aef12ae5181c

"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["User"]


import dataclasses, sqlite3

import flask
import flask_login

from . import db as DB
import library


@dataclasses.dataclass
class User(flask_login.UserMixin):

    user_id : int = ""
    username : str = ""
    password : str = dataclasses.field(default="", repr=False)   # Never stored.
    # salt_password : bytes = b""
    salt_password : bytes = dataclasses.field(default=b'', repr=False)
    email : str = ""
    is_admin : bool = False
    # https://flask-login.readthedocs.io/en/latest/#your-user-class
    is_active : bool = True

    user_id = None

    def get_id(self):
        return self.DB.get_user_from_email(self.email).user_id

    def __post_init__(self):
        #assure password is salted
        if self.password and isinstance(self.password, str):
            self.salt_password = library.salt_password(self.password)
        #Assign password property
        self.password = property(
            # lambda: raise ValueError("Cannot access user password."),
            lambda: None,
            lambda pw: setattr(self, "salt_password", library.salt_password(pw)),
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

    def __eq__(self, other):
        """Compare none property attributes."""
        for k,v in vars(self).items():
            if callable(v) or isinstance(v, property): continue
            try:
                if v != getattr(other, k):
                    print("This is the wrong attribute:", k, v)
                    return False
            except ValueError:
                return False
        return True or super(User).__eq__(other)

    class DB:

        _user_unique_fields = ['user_id', 'email', 'username']
 
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
                flask.flask(f"There was an error in retrieving the user via '{user_field}'.")
                return None

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
        def email_exists(cls, email : str) -> bool:
            """Confirms whether email exists."""
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
                if library.is_password(password, usr.salt_password):
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
                    salt_password=b'\x86\x98\xc8/=\x121\xd0\xf5E\xf0\x1b\xba\x17\xec\xe5\x0eG\xd3\x11\xc5O\xef\xf7\xbe\xd3\xa5\x80\x10\x85\xe6^',
                    email='example@example.com',
                ),
            ]
            for usr in users:
                conn = cls.insert_user(usr, commit=False)
            conn.commit()

        @classmethod
        def clear_users(cls, delete_admin=False):
            if delete_admin:
                sql = "DELETE FROM Users;"
            else:
                sql = "DELETE FROM Users WHERE is_admin=0;"
            db = cls.get_db()
            db.execute(sql)
            db.commit()
        

def get_user():
    """Similiar to 'get_db' function, get the current user."""
    if "user" not in flask.g:
        flask.g.user = User.DB.get_user_from_email(flask.session['_user_id'])
    return flask.g.user
        