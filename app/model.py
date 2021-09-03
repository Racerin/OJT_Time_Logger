"""Script containing other classes used in app.
I think it suppose to have SQLAlchemy in here. 
https://medium.com/analytics-vidhya/how-to-test-flask-applications-aef12ae5181c

"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["User"]


import dataclasses

import flask_login

import library


@dataclasses.dataclass
class User(flask_login.UserMixin):
    username : str = ""
    password : str = dataclasses.field(default="", repr=False)   # Never stored.
    # salt_password : bytes = b""
    salt_password : bytes = dataclasses.field(default=b'', repr=False)
    email : str = ""
    is_admin : bool = False
    # https://flask-login.readthedocs.io/en/latest/#your-user-class
    is_active : bool = True

    def get_id(self):
        return self.email

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
    def from_row1(cls, row) -> 'User':
        """Creates a user from a database row object."""
        try:
            usr = User(
                username=row['username'],
                salt_password=row['salt_password'],
                email=row['email'],
                )
        except TypeError:
            return None
        return usr

    @classmethod
    def from_row(cls, row) -> 'User':
        """Creates a user from a database row object."""
        usr = User(
            username=row['username'],
            salt_password=row['salt_password'],
            email=row['email'],
            is_admin=bool(row['is_admin'])
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