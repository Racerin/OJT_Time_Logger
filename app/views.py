import flask

from . import PARAM

def init_app(app):
    
    @app.route('/')
    def home():
        return flask.render_template(PARAM.HTML.HOME)
        # return "All my exes live in Texas."