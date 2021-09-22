import unittest
import os
import shutil
import tempfile
import sqlite3

import flask

import app as App
import app.db as DB


#Context managers to use
# with app.test_client() as test_client:     #https://werkzeug.palletsprojects.com/en/2.0.x/test/#werkzeug.test.Client
#     with test_client.session_transaction():  # https://flask.palletsprojects.com/en/2.0.x/api/#flask.testing.FlaskClient.session_transaction
#         with app.test_request_context('/route', data={}):   #https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.test_request_context
#             with app.app_context():


if __name__ == '__main__':
    unittest.main()