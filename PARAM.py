class HTML:
    HOME = "index.jinja-html"
    #user
    REGISTER = "/user/register.jinja-html"
    LOGIN = "user/login.jinja-html"
    SUCCESS = "user/success.jinja-html"
    LOGOUT = "/user/logout.jinja-html"
    SETTINGS = "user/settings.jinja-html"
    UNAUTH = "user/unauthorized_handler.jinja-html"
    STATUS = "user/status.jinja-html"
    EXECUTE = "user/execute.jinja-html"
    MESSAGE = "user/message.jinja-html"

class CONFIG:
    APP = "app.cfg"
    TEST = "test.cfg"
    # DEVELOPMENT = "development.cfg"

class DATABASE:
    FILENAME = "database.db"
    SCHEMA = "static/schema.sql"