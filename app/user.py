"""Contains the class and functions pertaining to website login user.
"""


__all__ = ["User"]
__author__ = "Darnell Baird"
__version__ = "0.1"


import dataclasses


@dataclasses.dataclass
class User():
    username : str = ""

    # Required properties for 'flask-login'.  # https://flask-login.readthedocs.io/en/latest/#your-user-class
    is_authenticated = False
    is_active = False
    is_anonymous = True
    @property.getter
    def get_id(self):
        return str(self.username).encode()