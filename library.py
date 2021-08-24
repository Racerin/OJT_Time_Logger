"""Module containing generic functions for application.
"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["check_email"]


import re
import hashlib

import config
import library


#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
email_patt = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_email(email) -> bool:
    """Determines if string is an email.
    """
    match = re.fullmatch(email_patt, email)
    if match:
        if match.group(0) == email:
            return True
    return False


#PASSWORD CONTROL
pw_salt = getattr(library.config, "SALT", "").encode("utf-8")


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