"""Module containing generic functions for application.
"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["check_email"]


import re


#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
email_patt = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check_email(email):
    return re.fullmatch(email_patt, email)