"""Flask Blueprint for authorizing user login.
"""


__author__ = "Darnell Baird"
# __all__ = ["bp", ]
__version__ = "0.1"


import flask
import flask_login
import flask_wtf        # http://wtforms.simplecodes.com/docs/0.6/fields.html#basic-fields
import wtforms

import library
import PARAM
from . import db
import model


login_manager = flask_login.LoginManager()


bp = flask.Blueprint('user', __name__, url_prefix="/user")


class UserLoginForm(flask_wtf.Form):
# class UserLoginForm(flask_wtf.FlaskForm):
    username_email = wtforms.StringField(
        label='Username/E-mail:', 
        validators=[
            wtforms.validators.DataRequired(),
            ]
        )
    password = wtforms.PasswordField(
        label='Password:',
        validators=[
            wtforms.validators.DataRequired(),
        ]
    )
    remember_me = wtforms.BooleanField(
        label="Remember Me:",
    )


class UserRegisterForm(UserLoginForm):
    password2 = wtforms.PasswordField(
        label='password2',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password', message="Passwords must match.")
        ]
    )
    email = wtforms.StringField(
        label='email',
        validators=[
            # wtforms.validators.Email()
        ]
    )


@login_manager.user_loader
def load_user(user_id) -> 'model.User':
    """Required callback function for linking a unique user_id
    to a user in the database.
    """
    #Get user row in database
    row = db.get_user(user_id)
    #Create user from row
    return model.User.from_row(row)

# @login_manager.request_loadeer
# def load_user_from_request(request):


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if flask.request.method == "POST":
        #Try to signup new user
        return "meh"
    #Just return the register page
    return "Register the user here."


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        flask.flash("The form data is valid.", 'error')
        #Get user
        if library.check_email(form.username_email.data):
            row = db.get_user_from_email(form.username_email.data)
        else:
            row = db.get_user_from_username(form.username_email.data)
        if row:
            flask.flash("We found the user in the database.", "debug")
            usr = model.User.from_row(row)
            #Setup 'Remember me'
            #Try to login the user
            if flask_login.login_user(usr):
                flask.flash("You have sucessfuly logged in.", 'info')
                return flask.redirect('/user/success')
            else:
                flask.flash(
                    "There was an error in logging in the user. \
                    Maybe problem within flask_login",
                     "error")
                return flask.redirect("/user/unsuccessful")
        else:
            flask.flash("We couldn't find the user in the database.", "error")
    #Just return the login page
    return flask.render_template(PARAM.HTML.LOGIN, form=form)


@bp.route("/logout")
def logout():
    # flask.session.clear()
    flask_login.logout_user()
    return flask.redirect( flask.url_for('home') )


@bp.route("/<string:name>")
def message(name):
    return flask.render_template(PARAM.HTML.MESSAGE, title=name)