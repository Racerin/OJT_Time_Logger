class HTML:
    HOME = "index.jinja-html"
    EXPERIMENT="experiment.jinja-html"
    CONTENT = "content.jinja-html"
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
    #clocking
    CLOCKING = 'clocking/clocking.jinja-html'
    CLOCKING_EDIT = 'clocking/edit.jinja-html'

class IMG:
    LOGO = "images/logo.png"
    dict1 = dict(LOGO=LOGO)

class CONFIG:
    APP = "app.cfg"
    TEST = "test.cfg"
    # DEVELOPMENT = "development.cfg"

class DATABASE:
    FILENAME = "database.db"
    SCHEMA = "static/schema.sql"

class CONSTANTS:
    SALT_ITERATIONS = int(1e6)