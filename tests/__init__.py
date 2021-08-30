import unittest
import os
import shutil
import tempfile


#Context managers to use
# with app.test_client() as test_client:     #https://werkzeug.palletsprojects.com/en/2.0.x/test/#werkzeug.test.Client
#     with test_client.session_transaction():  # https://flask.palletsprojects.com/en/2.0.x/api/#flask.testing.FlaskClient.session_transaction
#         with app.test_request_context('/route', data={}):   #https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.test_request_context
#             with app.app_context():


class TempDatabaseHandler():
    """Substitutes the original database for a temporary one of the same name.
    When closed, the original database is restored.
    """

    temp_db_filename = ""

    def __init__(self, db_filename):
        self.db_filename = db_filename
        #Copy and save original database away
        if os.path.exists(self.db_filename):
            self.file_obj, self.temp_db_filename = tempfile.mkstemp(suffix='.db')
            # shutil.copy(self.db_filename, self.temp_db_filename)
            os.system(f'cp {self.db_filename} {self.temp_db_filename}')

    def close(self):
        """Restore original database."""
        if os.path.exists(self.temp_db_filename):
            # shutil.copyfile(self.temp_db_filename, self.db_filename)
            os.system(f'cp {self.temp_db_filename} {self.db_filename}')

    def __del__(self):
        self.close()
        # super().__del__()     #no __del__ method
        # temp db file should be deleted automatically

if __name__ == '__main__':
    unittest.main()