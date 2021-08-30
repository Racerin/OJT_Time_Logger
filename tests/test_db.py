from sqlite3.dbapi2 import connect
import unittest
import os
import shutil
import tempfile
import sqlite3

import flask
import app as App
import app.model as app_model
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
        # del cls.temp_db_handler
        pass
    
    def test_get_db(self):
        #Initiate App
        app = App.create_app()
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

    def test_users(self):
        """Set and Get users from the database"""
        app = App.create_app()
        user1 = app_model.User(
            username="John Smith", 
            password="secret m3!",
            email="john@example.com",
            )
        with app.app_context():
            db.set_user(user1)
            user1_row = db.get_user_from_username("John Smith")
            user1_ret = app_model.User.from_row(user1_row)
            self.assertEqual(user1, user1_ret)
        

    def test_clock(self):
        pass


if __name__ == "__main__":
    unittest.main()