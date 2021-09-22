from sqlite3.dbapi2 import connect
import unittest
import os
import shutil
import tempfile
import sqlite3

import flask

import app as App
import app.db as DB


class TestGetDB(unittest.TestCase):
    
    
    def test_get_db(self):
        #Initiate App
        app = App.create_app(test_config=True)
        with app.app_context():
            connection = DB.get_db()
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