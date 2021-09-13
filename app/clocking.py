

import flask

import library
from . import db

bp = flask.Blueprint('clock', __name__, url_prefix='clocking')


bp.route("/")
def home():
    pass