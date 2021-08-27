from sqlite3.dbapi2 import connect
import unittest
import os
import shutil
import tempfile
import sqlite3

import flask

import app as App
import app.db as db

class TestGetDB(unittest.TestCase):
    
    orig_db_filename = 'database.db'
    temp_db_filename = ""

    @classmethod
    def setUpClass(cls):
        #Copy and save original database away
        if os.path.exists(cls.orig_db_filename):
            _, cls.temp_db_filename = tempfile.mkstemp(suffix='.db')
            shutil.copy(cls.orig_db_filename, cls.temp_db_filename)

    @classmethod
    def tearDownClass(cls):
        #Restore original database
        if os.path.exists(cls.temp_db_filename):
            shutil.copy(cls.temp_db_filename, cls.orig_db_filename)
            # temp db file should be deleted automatically
    
    def test_get_db(self):
        #Initiate App
        app = App.create_app()
        with app.test_client() as client:
            with app.app_context() as app_context:
                connection = db.get_db()
                self.assertIsInstance(connection, sqlite3.Connection)
                self.assertTrue(issubclass(connection.row_factory, sqlite3.Row))
                #Assert Admin User
                sql = "SELECT username, salt_password, email, is_active, is_admin FROM Users WHERE is_admin=1;"
                rows = connection.execute(sql)
                n_admins = 0
                for i, row in enumerate(rows):
                    n_admins += 1
                    admin_row = row
                    print(row['is_admin'])
                self.assertEqual(n_admins, 1, msg="There should only be one admin.")
                self.assertEqual(admin_row['is_admin'], 1)
                self.assertEqual(admin_row['username'], 'admin')
                #Test Users
                #Test Clock


if __name__ == "__main__":
    unittest.main()