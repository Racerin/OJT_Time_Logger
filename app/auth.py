"""Flask Blueprint for authorizing user login.
"""


__author__ = "Darnell Baird"
__all__ = ["bp", ]
__version__ = "0.1"


import flask

import user


bp = flask.blueprint('auth', __name__, url_prefix="auth")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if flask.request.method == "POST":
        #Try to signup new user
        pass
    #Just return the login page
    return "Register the user here."


@bp.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        #Try to login the user
        pass
    #Just return the login page
    return "Login the user"


@bp.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect( flask.url_for('home') )