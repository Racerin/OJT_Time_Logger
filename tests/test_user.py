import unittest

import app as App


class TestUser(unittest.TestCase):
    
    def test_sign_in_out(self):
        app = App.create_app(test_config=True)
        with app.test_client() as client:
            # with app.app_context() as app_context:
            client.post("user/login")


class TestAdminUser(TestUser):
    
    def test_sign_in_out(self):
        pass

    def test_register(self):
        pass

    def test_privileges(self):
        pass


if __name__ == "__main__":
    unittest.main()