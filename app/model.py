"""Script containing other classes used in app.
"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["User"]


import dataclasses

import flask_login

import library


@dataclasses.dataclass
# class User(flask_login.UserMixin):
class User(flask_login.AnonymousUserMixin):
    username : str = ""
    password : str = ""   # Never stored.
    salt_password : bytes = b""
    email : str = ""

    # Required properties for 'flask-login'.  # https://flask-login.readthedocs.io/en/latest/#your-user-class
    # is_authenticated = False
    # is_active = False
    # is_anonymous = True
    # @property.getter
    # def get_id(self) -> bytes:
    #     return str(self.username).encode()

    # Password Management
    @property
    def password(self):
        raise ValueError("Cannot access user password.")

    @password.setter
    def password(self, password):
        """Password is never stored in object. Password is salted.
        """
        # Set salted password.
        self.salt_password = library.salt_password(password)

    @property
    def user_id(self):
        return self.email

    @user_id.setter
    def user_id(self, val):
        pass

    def __post_init__(self):
        #assure password is salted
        try:
            if self.password:
                self.salt_password = library.salt_password(self.password)
        except:
            print("I told you so.")


    @classmethod
    def from_row(cls, row) -> 'User':
        """Creates a user from a database row object."""
        usr = User(
            username=row['username'],
            salt_password=row['salt_password'],
            email=row['email'],
            )
        return usr

