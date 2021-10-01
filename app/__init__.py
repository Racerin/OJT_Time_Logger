"""Flask app package.
Web application for OJT Trainee Time Logging.
"""


__author__ = "Darnell Baird"
__version__ = "0.1"
__all__ = ["create_app", ]


import toml
import os
import tempfile
import atexit
import urllib.parse

import flask
import click

import PARAM
import library
import configmodule
from . import db


def create_app(test_config=False) -> flask.Flask:
    """Create and configure an instance of the Flask application. """
    app = flask.Flask(__name__, instance_relative_config=True)

    # Configurations
    app.testing = test_config
    if app.testing:
        app.config.from_object(configmodule.TestingConfig)
        # Create a test database
        _, app.config['DATABASE'] = tempfile.mkstemp(suffix='.db')
        with app.app_context():
            db.init_db()
        # Delete database when finished
        atexit.register(library.del_file, filename=app.config['DATABASE'])
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

    # Add PARAM to jinja global variables
    @app.context_processor
    def add_PARAM() -> dict:
        """Adds PARAM constants to jinja template."""
        return dict(IMG=PARAM.IMG)

    # Add breadcrumbs to jinja global variables
    @app.context_processor
    def add_breadcrumbs() -> dict:
        """Create and return a dict containing a list of breadcrumbs."""
        host_url = flask.request.host_url
        path = flask.request.path
        # Split path destinations
        destinations = [s for s in os.path.split(path) if bool(s)]
        n_destinations = len(destinations)
        breadcrumbs = list()
        for i in range(n_destinations):
            # Accumulate-url-join each list of destinations to create sub-paths
            sub_paths = destinations[:i+1]
            sub_path = r'/'.join(sub_paths)
            breadcrumb = urllib.parse.urljoin(host_url, sub_path)
            breadcrumbs.append(breadcrumb)
        return dict(breadcrumbs=breadcrumbs)


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

    # Add local commands
    app.cli.add_command(generate_secret_key_command)
    
    return app


@click.command('gen-secret-key')
@flask.cli.with_appcontext
@click.argument("length", type=int, default=20)
def generate_secret_key_command(length=20):
    """Generate a secret key to use in flask."""
    ans = os.urandom(length).hex()
    print(ans)
    # return 