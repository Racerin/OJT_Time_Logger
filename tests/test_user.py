import unittest

import flask

import app as App

from . import TempDatabaseHandler
from instance import config as instance_config

import app.user as app_user


class TestPages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_db_handler = TempDatabaseHandler('database.db')

    @classmethod
    def tearDownClass(cls):
        del cls.temp_db_handler

    def setUp(self):
        self.app = App.create_app(test_config=True)

    def tearDown(self):
        return super().tearDown()

    def test_register(self):
        """Test user register page."""
        #Set up
        self.app.config["WTF_CSRF_ENABLED"] = False
        client = self.app.test_client()
        #1st time
        resp = client.get("user/register")
        # print("Dir of resp.", dir(resp))
        html = resp.data.decode()
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Register", html)
        #Signup
        with self.app.test_request_context() as request:
            form = app_user.UserRegisterForm(data={
                'username':'Kazoo',
                'email':'kazoo@gmail.com',
                'password1':'Password@1234!',
                'password2':'Password@1234!',
            })
            # print("This is form.data:", form.data)
            resp = client.post(
                "user/register", 
                data=form.data,
                # data=dict(**form.data, login_form=""),
                follow_redirects=True,
                )
            html = resp.data.decode()
            # print("This is form: ", dir(resp.request))
            self.assertEqual(resp.status_code, 200)
            assert 'required' not in html, html
            assert "Success" in html, html
            #Signup fail
            resp = client.post("user/register", form=form)
            html = resp.data.decode()
            self.assertEqual(resp.status_code, 300)
            self.assertIn("exists", html.lower())


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_db_handler = TempDatabaseHandler('database.db')

    @classmethod
    def tearDownClass(cls):
        del cls.temp_db_handler

    def setUp(self) -> None:
        self.app = App.create_app(test_config=True)

    def tearDown(self) -> None:
        pass
    
    def test_sign_in_out(self):
        """Ensure user can log in and out, and is with correct privileges."""
        client = self.app.test_client()
        #GET user login webpagepage
        resp = client.get(
            "user/login", 
            content_type='html/text'
            )
        # print("Flask request data:", resp.request.data)
        self.assertEqual(resp.status_code, 200)
        # self.print_response_options(get_login_resp)
        session = client.session_transaction()
        # print("This is after client's GET session:", session, "session dir:", dir(session))
        #POST login user webpage
        post_data = {
            'username':"FooBar",
            'password':instance_config.FOO_USER_PASSWORD,
            # 'password':'dog',
            "login_form":"",
        }
        post_login_resp = client.post(
            "user/login", 
            data=post_data, 
            follow_redirects=True,
            )
        # self.print_response_options(post_login_resp, print_dir=False)
        self.assertEqual(post_login_resp.status_code, 200)
        """ self.assertNotEqual(
            get_login_resp.data, 
            post_login_resp.data,
            msg="The webpage between post and get methods is the same."
            )
        self.assertTrue(
            b'Success' in post_login_resp.data or b'success' in post_login_resp.data,
            msg="This is not the success page."
            ) """

    def test_sign_in_out2(self):
        with self.app.test_client() as client:
            with client.session_transaction() as session:
                pass
                # print("Client Session:", session)
        get_request = self.app.test_request_context()
        get_request.push()
        get_request.pop()

    def test_register(self):
        """Register a user."""
        pass

    def print_response_options(self, response, print_dir=True):
        if print_dir:
            print(f"Response '{response}' dir: {dir(response)}")
        info = [
            'status', 'status_code',
            'history',
            'expires',
            'data',
            'headers',
        ]
        print("="*50)
        for tag in info:
            rep_tag = tag.replace('_',' ').title()
            print(f"{rep_tag}: {getattr(response, tag)}")


class TestAdminUser(TestUser):

    @classmethod
    def setUpClass(cls):
        cls.temp_db_handler = TempDatabaseHandler('database.db')

    @classmethod
    def tearDownClass(cls):
        del cls.temp_db_handler

    def test_sign_in_out(self):
        """Ensure admin could sign in and out with correct privilages?"""
        with self.app.test_client() as client:
            pass

    def test_privileges(self):
        pass


if __name__ == "__main__":
    unittest.main()