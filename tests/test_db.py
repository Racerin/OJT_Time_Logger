from sqlite3.dbapi2 import connect
import unittest
import os
import shutil
import tempfile
import sqlite3

import flask

import app as App
import app.db as db

from . import TempDatabaseHandler


class TestGetDB(unittest.TestCase):
    
    orig_db_filename = 'database.db'

    @classmethod
    def setUpClass(cls):
        #Copy and save original database away
        cls.temp_db_handler = TempDatabaseHandler(cls.orig_db_filename)

    @classmethod
    def tearDownClass(cls):
        #Restore original database
        del cls.temp_db_handler     #must be explicit
    
    def test_get_db(self):
        #Initiate App
        app = App.create_app()
        with app.app_context():
            connection = db.get_db()
            self.assertIsInstance(connection, sqlite3.Connection)
            self.assertTrue(issubclass(connection.row_factory, sqlite3.Row))

    def test_close_db(self):
        pass

    def test_init_db(self):
        pass
        

    def test_clock(self):
        pass


if __name__ == "__main__":
    unittest.main()