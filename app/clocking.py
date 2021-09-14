

import flask

import library
import PARAM
from . import db
from . import user
from . import model


bp = flask.Blueprint('clocking', __name__, url_prefix='/clocking')


class ClockForm():
    def __init__(self):
        user_id = model.get_user().user_id
        self.is_clocked_in = db.is_clocked_in(user_id)
        self.last_clock_in = db.last_clock_in(user_id)
        # self.last_clock_in = "Today"


@bp.route("/")
@user.flask_login.login_required
def home():
    return flask.render_template(
        PARAM.HTML.CLOCKING, 
        form=ClockForm(),
        )


@bp.route("/clock_out", methods=['POST'])
@user.flask_login.login_required
def clock_out():
    db.clock_out(model.get_user().user_id)
    return flask.redirect( flask.url_for("home") )


@bp.route("/clock_in", methods=['POST'])
@user.flask_login.login_required
def clock_in():
    current_user = model.get_user()
    db.clock_in(current_user.email)
    return flask.redirect( flask.url_for("home") )


@bp.route("/<string:str1>")
def anything(str1):
    return f"This is the string; \n'{str1}'"


def init_app(app):
    pass