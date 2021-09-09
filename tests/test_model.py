import unittest

import flask

import app as App
import app.model as app_model
import app.db as db

from . import TempDatabaseHandler
from instance import config as instance_config


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_db_handler = TempDatabaseHandler('database.db')

    @classmethod
    def tearDownClass(cls):
        del cls.temp_db_handler #must be explicit

    def test_users(self):
        """Set and Get users from the database"""
        app = App.create_app()
        user1 = app_model.User(
            username="John Smith", 
            password="secret m3!",
            email="john@example.com",
            )
        with app.app_context():
            db.insert_user(user1)
            user1_row = db.get_user_from_username("John Smith")
            user1_ret = app_model.User.from_row(user1_row)
            self.assertEqual(user1, user1_ret)

    def test_admin(self):
        #Assert Admin User
        sql = "SELECT username, salt_password, email, is_active, is_admin FROM Users WHERE is_admin=1;"
        connection = db.get_db()
        rows = connection.execute(sql)
        n_admins = 0
        for i, row in enumerate(rows):
            n_admins += 1
            admin_row = row
            print(row['is_admin'])
        self.assertEqual(n_admins, 1, msg="There should only be one admin.")
        self.assertEqual(admin_row['is_admin'], 1)
        self.assertEqual(admin_row['username'], 'admin')
