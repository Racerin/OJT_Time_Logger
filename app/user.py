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
from . import model


login_manager = flask_login.LoginManager()


bp = flask.Blueprint('user', __name__, url_prefix="/user")


class UserLoginForm(flask_wtf.FlaskForm):
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


class UserRegisterForm(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        label="Username: ",
        validators=[
            wtforms.validators.DataRequired(),
        ]
    )
    password1 = wtforms.PasswordField(
        label='Enter Password: ',
        validators=[
            wtforms.validators.DataRequired(),
            # wtforms.validators.EqualTo('password', message="Passwords must match.")
        ]
    )
    password2 = wtforms.PasswordField(
        label='Enter Password Again:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password1', message="Passwords must match.")
        ]
    )
    email = wtforms.StringField(
        label='E-mail: ',
        validators=[
            # wtforms.validators.Email()
        ]
    )


class UserSettingsForm(flask_wtf.FlaskForm):
    new_username = wtforms.StringField()
    current_email = wtforms.StringField()
    new_email = wtforms.StringField()
    current_password1 = wtforms.PasswordField()
    current_password2 = wtforms.PasswordField()


@login_manager.user_loader
def load_user(email) -> 'model.User':
    """This callback is used to reload the user object
     from the user ID stored in the session.
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    """
    #Get user row in database
    row = db.get_user_from_email(email)
    #Create user from row
    return model.User.from_row(row)

# @login_manager.request_loadeer
# def load_user_from_request(request):

@login_manager.unauthorized_handler
def unauthorized_handler():
    """View returned if user failed ot log in."""
    flask.flash("Invalid User login.")
    return flask.render_template(PARAM.HTML.UNAUTH)
    # return flask.redirect(PARAM.HTML.UNAUTH)


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
        flask.flash("The form data is valid.", 'debug')
        #Get user
        username_email = form.username_email.data
        if library.is_email(username_email):
            row = db.get_user_from_email(username_email)
        else:
            row = db.get_user_from_username(username_email)
        if row:
            flask.flash("We found the user in the database.", "debug")
            usr = model.User.from_row(row)
            flask.flash("This is user: {}".format(usr))
            #Setup 'Remember me'
            #Try to login the user
            if flask_login.login_user(usr):
                flask.flash("You have sucessfuly logged in.", 'info')
                # return flask.redirect( '/user/success' )
                # return flask.redirect( flask.url_for('user.success') )
                return flask.render_template(PARAM.HTML.SUCCESS)
            else:
                flask.flash(
                    "There was an error in logging in the user. \
                    Maybe problem within flask_login.",
                     "error")
                return flask.redirect("/user/unsuccessful")
        else:
            flask.flash("We couldn't find the user in the database.", "error")
    else:
        flask.flash("The form data is invalid.", 'debug')
    #Just return the login page
    return flask.render_template(PARAM.HTML.LOGIN, form=form)


@bp.route("/success")
@flask_login.login_required
def success():
    """Display to user that they are logged in."""
    return flask.render_template( PARAM.HTML.SUCCESS )


@bp.route("/logout", methods=['POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect( flask.url_for('home') )


@bp.route("/settings", methods=["POST", "GET"])
@flask_login.login_required
def settings():
    form = UserSettingsForm()
    if flask.request.method == "POST":
        #Save the user Settings
        flask.redirect( flask.url_for('home') )
    #Return users settings page
    return flask.render_template(PARAM.HTML.SETTINGS, form=form)


@bp.route("/<string:name>")
def message(name):
    """Generic template to return webpage with flash messages."""
    return flask.render_template(PARAM.HTML.MESSAGE, title=name)


def init_app(app):
    """Instantiate packages/modules with app of instance."""
    login_manager.init_app(app)