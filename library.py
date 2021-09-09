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


def salt_password(pw: 'str|bytes', iterations=int(1e6)) -> bytes:
    """Salts password using pbkdf2_hmac."""
    if len(pw) == 0:
        raise ValueError("Password must be longer than 0.")
    # https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    b_password = pw if isinstance(pw, bytes) else pw.encode('utf-8')
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256', 
        password=b_password, 
        salt=pw_salt, 
        iterations=iterations,
        )
    return key


def is_password(password : str, salted : bytes):
    """Compare a new password to the salted value"""
    salted_password = salt_password(password)
    return salted_password == salted


def has_digit(str1 : str) -> bool:
    """String contains a digit."""
    if not isinstance(str1, str):
        raise TypeError(f"Input '{str1}' must be of type 'str'.")
    return any(d.isdigit() for d in str1) and len(str1) > 0


def has_letter(str1 : str) -> bool:
    """String contains a letter."""
    if not isinstance(str1, str):
        raise TypeError(f"Input '{str1}' must be of type 'str'.")
    return any(s.isalpha() for s in str1) and len(str1) > 0


def has_symbol(str1 : str) -> bool:
    """String contains a symbol."""
    if not isinstance(str1, str):
        raise TypeError(f"Input '{str1}' must be of type 'str'.")
    # return any(not l.isdigit() and not l.isalpha() and l.isprintable() for l in str1)
    return bool(re.search(
        r'[!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~]',
        str1,
        ))