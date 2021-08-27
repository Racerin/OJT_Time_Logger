import unittest
import os
import shutil
import tempfile
import sqlite3

import app.db

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
        connection = app.db.get_db()
        self.assertIsInstance(connection, sqlite3.Connection)
        self.assertIsInstance(connection.row_factory, sqlite3.Row)
        #Assert Admin User
        sql = "SELECT username, salt_password, email, is_active FROM Users WHERE is_admin=1;"
        rows = connection.execute(sql)
        n_admins = len(rows)
        self.assertEqual(n_admins, 1)
        admin_row = rows[0]
        self.assertEqual(admin_row['is_admin'], 1)
        self.assertEqual(admin_row['username'], 'admin')
        #Test Users
        #Test Clock
    
    def test_goat(self):
        print("A test was done.")


if __name__ == "__main__":
    unittest.main()