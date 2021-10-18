class HTML:
    HOME = "index.jinja-html"
    EXPERIMENT="experiment.jinja-html"
    CONTENT = "content.jinja-html"
    #user
    USER = "/user/index.jinja-html"
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

class FORM:
    USRNM_RNG = (2,60)
    PW_RNG = (8,60)
    VLDR_MSGS = {
        'em_used':"E-mail already in use.",
        'plz_val_em':"Please enter a valid e-mail address.",
        'unm_l_rg':"Username must be between {} and {} characters long.",
        'pw_l_rg':"Password must be between {} and {} characters long.",
        'pw_match':"Passwords must match.",
        'em_match':"E-mail must match.",
        'unm_no_wht_spc':"Username cannot contain any whitespace.",
        'pw_d_w_s':"Password requires atleast a number, letter and symbol.",
    }

class LIMITS:
    RECENT_CLOCK_DATA = 10