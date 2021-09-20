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
import configmodule
from . import db


def create_app(test_config=False) -> flask.Flask:
    """Create and configure an instance of the Flask application. """
    app = flask.Flask(__name__, instance_relative_config=True)

    # Configurations
    app.testing = test_config
    if app.testing:
        app.config.from_object(configmodule.TestingConfig)
    elif app.config['ENV'] == 'development':
        app.config.from_object(configmodule.DevelopmentConfig)
    elif app.config['ENV'] == 'production':
        app.config.from_object(configmodule.ProductionConfig)
    else:
        app.config.from_object(configmodule.Config)
    # Config with environment variable
    app.config.from_envvar('FLASK_SECRET_KEY', silent=True)
    # Load 'instance' folder's config. Do NOT include 'instance in production code. 
    if not app.config.from_pyfile('config.py', silent=True):
        app.logger.warning("'instance/config' could not be found.")

    # Views
    # from . import views
    import app.views as temp_views
    temp_views.init_app(app)

    #Initialize Plugins
    #Add database
    db.init_app(app)
    
    # Apply blueprints to the app
    #flask-login and auth
    from . import user
    app.register_blueprint(user.bp)
    user.init_app(app)
    #clock
    from . import clocking
    app.register_blueprint(clocking.bp)
    # clocking.init_app(app)
    
    return app