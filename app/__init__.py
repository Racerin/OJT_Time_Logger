"""Flask app package.
Web application for OJT Trainee Time Logging.
"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["create_app", ]


import toml
import os

import flask

import PARAM
from . import db


def create_app(test_config=False):
    """Create and configure an instance of the Flask application. """
    app = flask.Flask(__name__, instance_relative_config=True)

    #Configurations
    app.config.from_object('config')
    #load 'instance' folder config. Do NOT include 'instance in production code. 
    app.config.from_envvar('FLASK_SECRET_KEY', silent=True)
    if not app.config.from_pyfile('config.py', silent=True):
        app.logger.warning("Instance config could not be found.")

    #Views
    # from . import views
    import app.views as temp_views
    temp_views.init_app(app)

    #Initialize Plugins
    #Add database
    db.init_app(app)
    
    #Apply blueprints to the app
    #flask-login and auth
    from . import user
    app.register_blueprint(user.bp)
    user.login_manager.init_app(app)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()