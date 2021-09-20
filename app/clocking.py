

import flask

import library
import PARAM
from . import db
from . import user
from . import model


bp = flask.Blueprint('clocking', __name__, url_prefix='/clocking')


class ClockForm():
    def __init__(self):
        user_id = getattr(model.get_user(), 'user_id', None)
        self.is_clocked_in = db.is_clocked_in(user_id)
        self.last_clock_in = db.last_clock_in(user_id)

    def last_clock_in_nice(self):
        """Returns a nice-looking string of the 
        'last_clock_in' return value.
        """
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        # str1 = self.last_clock_in.strftime('%c')
        str1 = self.last_clock_in.strftime('%A %d %b, %I:%M %p')
        return str1


@bp.route("/")
@user.flask_login.login_required
def home():
    clock_form = ClockForm()
    return flask.render_template(
        PARAM.HTML.CLOCKING, 
        form=clock_form,
        )


@bp.route("/clock_out", methods=['POST'])
@user.flask_login.login_required
def clock_out():
    user_id = getattr(model.get_user(), 'user_id', None)
    db.clock_out(user_id)
    return flask.redirect( flask.url_for("home") )


@bp.route("/clock_in", methods=['POST'])
@user.flask_login.login_required
def clock_in():
    user_id = getattr(model.get_user(), 'user_id', None)
    db.clock_in(user_id)
    return flask.redirect( flask.url_for("home") )


@bp.route("/submits", methods=['GET', 'POST'])
@model.user.admin_access
def edit():
    if flask.request.method == 'POST':
        pass
    return PARAM.HTML.EDIT


@bp.route("/<string:str1>")
def anything(str1):
    return f"This is the string; \n'{str1}'"


def init_app(app):
    pass