import unittest

import flask

import app as App
import app.model as app_model
import app.db as DB

from . import TempDatabaseHandler
from instance import config as instance_config


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_db_handler = TempDatabaseHandler('database.db')

    @classmethod
    def tearDownClass(cls):
        del cls.temp_db_handler #must be explicit

    def setUp(self):
        self.app = App.create_app(test_config=True)
        self.test_client = self.app.test_client()

    def test_users(self):
        """Insert, Select, and Delete users from the database"""
        user1 = app_model.User(
            username="John Smith", 
            password="secret m3!",
            email="john@example.com",
            )
        with self.app.test_request_context():
            # Insert user
            app_model.User.DB.insert_user(user1)
            # self.assertTrue(app_model.DB.email_exists(user1.email))   #Not tested as yet
            # Get User
            user1_ret_email = app_model.User.DB.get_user_from_email(user1.email)
            user1_ret_username = app_model.User.DB.get_user_from_username(user1.username)
            user1_ret_username_email_email = app_model.User.DB.get_user_from_username_email(user1.email)
            user1_ret_username_email_username = app_model.User.DB.get_user_from_username_email(user1.username)
            self.assertEqual(user1, user1_ret_email)
            self.assertEqual(user1, user1_ret_username)
            self.assertEqual(user1, user1_ret_username_email_email)
            self.assertEqual(user1, user1_ret_username_email_username)
            # Delete User 
            # (ATM, no function). clean-up
            # sql = "DELETE FROM Users WHERE email=john@example.com"
            sql = "DELETE FROM Users WHERE user_id = (SELECT MAX(user_id) FROM Users);"
            DB.get_db().execute(sql)
            DB.get_db().commit()

    def test_admin(self):
        # Admin User exists and is valid
        sql = "SELECT username, salt_password, email, is_active, is_admin FROM Users WHERE is_admin=1;"
        with self.app.test_request_context():
            connection = DB.get_db()
            rows = connection.execute(sql)
            n_admins = 0
            for row in rows:
                n_admins += 1
                admin_row = row
                print(row['is_admin'])
            self.assertEqual(
                n_admins, 1, 
                msg=f"There should be one admin. {n_admins} found.")
            self.assertEqual(admin_row['is_admin'], 1)
            self.assertEqual(admin_row['username'], 'admin')
