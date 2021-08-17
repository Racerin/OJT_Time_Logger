import toml
import os

import flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis
import flask_login

# from Library import Database
from . import PARAM
from . import db
import user


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
    @app.route('/')
    def home():
        return "All my exes live in Texas."

    #Initialize Plugins
    #Add database
    db.init_app(app)
    
    #Apply blueprints to the app
    #User authentication
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()