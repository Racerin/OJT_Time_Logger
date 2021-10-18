import flask

from . import PARAM

def init_app(app):
    
    @app.route('/')
    def home():
        return flask.render_template(PARAM.HTML.HOME)

    @app.route('/experiment')
    def experiment():
        return flask.render_template(PARAM.HTML.EXPERIMENT)

    @app.route("/help")
    def help():
        """Help page for doc."""
        return flask.render_template(PARAM.HTML.HELP)