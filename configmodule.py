import datetime
import tempfile


class Config:

    TESTING = False
    DEBUG = False
    SECRET_KEY = "Please change me to something more secret."

    RECAPTCHA_PUBLIC_KEY = "Get this from Google recaptcha"
    RECAPTCHA_PRIVATE_KEY = "I think your site must be public."

    DATABASE = "database.db"
    SALT = "salt"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "password"


    # Login
    # REMEMBER_COOKIE_DURATION = 6
    # REMEMBER_COOKIE_DURATION = datetime.timedelta(days=6)


    #Forms
    # WTF_CSRF_ENABLED = False
    # WTF_CSRF_SECRET_KEY = 'a random string'


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE = 'test.db'


class DevelopmentConfig(Config):
    # DATABASE = 'test.db'
    WTF_CSRF_ENABLED = False
    pass


class ProductionConfig(Config):
    pass