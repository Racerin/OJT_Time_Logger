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
login_manager.refresh_view = "user.reauthenticate"
login_manager.login_view = "user.login"
login_manager.login_message = "Please log in before proceeding."


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
        label="Keep me logged in:",
    )


class UserRegisterForm(flask_wtf.FlaskForm):

    _usrnm_range = (5,60)
    _pw_range = (8,60)

    username = wtforms.StringField(
        label="Username: ",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(
                min=_usrnm_range[0], 
                max=_usrnm_range[1],
                message=
                "Username must be between {} and {} characters long."
                    .format(*_usrnm_range)
                ),
        ]
    )
    """ email = wtforms.fields.html5.Email(
        label='E-mail: ',
    ) """
    email = wtforms.StringField(
        label='E-mail: ',
        validators=[
            # wtforms.validators.Email(),
            wtforms.validators.DataRequired(),
        ]
    )
    password1 = wtforms.PasswordField(
        label='Enter Password: ',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(
                min=_pw_range[0], 
                max=_pw_range[1], 
                message=
                "Password must be between 8 and 60 characters long."\
                    .format(*_pw_range)
                ),
        ]
    )
    password2 = wtforms.PasswordField(
        label='Enter Password:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo(
                'password1', message="Passwords must match."
                )
        ]
    )
    recaptcha = flask_wtf.RecaptchaField()

    def validate_username(self, field : wtforms.fields.Field):
        """A special method automatically called when
        validating the 'usrname' field.
        No whitespace in username.
        """
        if library.re.findall(r'/s', field.data):
            raise wtforms.validators.ValidationError("Username cannot include any whitespace.")

    def validate_email(self, field : wtforms.fields.Field):
        """A special method automatically called when
        validating the 'email' field.
        Regex evaluation of email.
        User/email exists.
        """
        if not library.is_email(field.data):
            raise wtforms.validators.ValidationError("Please enter a valid e-mail address.")
        if db.email_exists(field.data):
            raise wtforms.validators.ValidationError("E-mail already in use.")

    def validate_password1(self, field : wtforms.Field):
        """A special method automatically called when
        validating the 'password1' field.
        Password must contain numbers, characters, symbols.
        """
        bools = [f(field.data) for f in [library.has_digit, library.has_letter, library.has_symbol]]
        if not all(bools):
            raise wtforms.validators.ValidationError("Password requires atleast a number, letter and symbol.")
        # if not library.has_digit(field.data):
        #     raise wtforms.validators.ValidationError("Password requires a digit.")
        # if not library.has_letter(field.data):
        #     raise wtforms.validators.ValidationError("Password requires a character.")
        # if not library.re.findall(r'[!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~]', field.data):
        #     raise wtforms.validators.ValidationError("Password requires a punctuation.")



class UserSettingsForm(flask_wtf.FlaskForm):
    new_username = wtforms.StringField()
    current_email = wtforms.StringField()
    new_email = wtforms.StringField()
    current_password1 = wtforms.PasswordField()
    current_password2 = wtforms.PasswordField()


@login_manager.user_loader
def load_user(username_email) -> 'model.User':
    """This callback is used to reload the user object
     from the user ID stored in the session.
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    """
    #Get user row in database
    row = db.get_user_from_username_email(username_email)
    #Create user from row
    return model.User.from_row(row)


@login_manager.unauthorized_handler
def unauthorized_handler():
    """View returned if user failed ot log in."""
    flask.flash("Invalid User login.")
    return flask.render_template(PARAM.HTML.UNAUTH)


@bp.route("/reauthenticate")
def reauthenticate():
    """If a user is still logged in with their cookies 
    but closed the website (stale),
    the user is redirected to this view if re-login is required.
    https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.refresh_view"""
    flask.flash("Please sign-in again.", "login")
    flask.redirect( "/user/login" )


@bp.route("/register", methods=['GET', 'POST'])
def register():
    """User Register webpage view and client handling."""
    form = UserRegisterForm()
    if form.validate_on_submit() and flask.request.method == "POST":
        #Signup new user
        if db.email_exists(form.email.data):
            flask.flash("User already exists.", "error")
            return flask.redirect( "/user/register" )
        usr = model.User.from_register_form(form)
        #Insert into database
        db.insert_user(usr)
        #Success
        flask.flash("User registered.", 'success')
        return flask.redirect("/user/register_success")
    return flask.render_template(PARAM.HTML.REGISTER, form=form)


@bp.route("/register_success")
def register_success():
    statement = "Welcome user. Check your e-mail to activate your account."
    return flask.render_template(PARAM.HTML.SUCCESS, statement=statement)


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit() and flask.request.method == "POST":
        flask.flash("The form data is valid.", 'debug')
        #Get user id
        username_email = form.username_email.data
        password = form.password.data
        remember_me = form.remember_me.data
        row = db.login(username_email, password)
        if row:
            flask.flash("Valid user login.", "debug")
            usr = model.User.from_row(row)
            if flask_login.login_user(usr, remember=remember_me):
                flask.flash("You have successfuly logged in.", 'info')
                return flask.redirect( flask.url_for("home") )
            else:
                flask.flash(
                    "There was an error in logging in the user. \
                    Maybe problem within flask_login.",
                     "error")
                return flask.redirect("/user/login")
        else:
            flask.flash("We couldn't find the user in the database.", "error")
            return flask.redirect("/user/login")
    else:
        flask.flash("The form data is invalid.", 'debug')
    return flask.render_template(PARAM.HTML.LOGIN, form=form)


@bp.route("/success")
@flask_login.login_required
def success():
    """Display to user that they are logged in."""
    return flask.render_template( PARAM.HTML.SUCCESS )


@bp.route("/logout", methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect( flask.url_for('home') )


@bp.route("/settings", methods=["POST", "GET"])
@flask_login.login_required
@login_manager.needs_refresh_handler
def settings():
    form = UserSettingsForm()
    if flask.request.method == "POST":
        #Save the user Settings
        flask.redirect( flask.url_for('home') )
    #Return users settings page
    return flask.render_template(PARAM.HTML.SETTINGS, form=form)


@bp.route("/status")
def status():
    return flask.render_template( PARAM.HTML.STATUS )

@bp.route("/execute", methods=['POST', 'GET'])
def execute():
    """Pass a text input to execute any script
    NB: THIS PAGE IS EXTREMELY DANGEROUS.
    """
    if flask.request.method == "POST":
        str1 = flask.request.form['line']
        if str1:
            flask.flash(str1, "last_input")
        exec(str1)
    return flask.render_template( PARAM.HTML.EXECUTE )


@bp.route("/<string:name>")
def message(name):
    """Generic template to return webpage with flash messages."""
    return flask.render_template(PARAM.HTML.MESSAGE, title=name)


def init_app(app):
    """Instantiate packages/modules with app of instance."""
    app.config["RECAPTCHA_PUBLIC_KEY"] = "-w0g968n-9eru0nb-0-098n-8"
    login_manager.init_app(app)
    pass