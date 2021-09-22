import unittest

import flask

import app as App
import app.db as DB

from instance import config as instance_config

import app.user as app_user


class TestUser(unittest.TestCase):

    vldr_msgs = app_user.UserRegisterForm._vldr_msgs

    def setUp(self):
        self.app = App.create_app(test_config=True)

    def test_register(self):
        """Test user register page."""
        # Set up
        client = self.app.test_client()
        # 1st time, Register page
        resp = client.get("user/register")
        html = resp.data.decode()
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Register", html)
        # Signup
        with self.app.test_request_context():
            form = app_user.UserRegisterForm(data={
                'username':'Kazoo',
                'email':'kazoo@gmail.com',
                'password1':'Password@1234!',
                'password2':'Password@1234!',
            })
            resp = client.post(
                "user/register", 
                data=form.data,
                follow_redirects=True,
                )
            html = resp.data.decode()
            self.assertEqual(resp.status_code, 200)
            assert 'Register' not in html, html
            assert "Success" in html, html
            # 2nd Signup fail
            resp = client.post(
                "user/register", 
                data=form.data,
                follow_redirects=True,
                )
            html = resp.data.decode()
            self.assertEqual(resp.status_code, 200)
            assert form._vldr_msgs['em_used'] in html, html     #E-mail already in use.

    def test_bad_register(self):
        """Test the response due to bad registering of users.
        Use 'test_register' for reference.
        """
        # Set up
        client = self.app.test_client()
        # Post a valid email
        with self.app.test_request_context():
            dict1 = dict(username="Ringo",email="ringo@example.com", password1="Ringo4L!fe", password2="Ringo4L!fe")
            valid_form = app_user.UserRegisterForm(data=dict1)
            client.post("user/register", data=valid_form.data, follow_redirects=True,)
        # Input variables
        datas = [
            dict(username="", email="fb@eg.com", password="foobar!123", password2="foobar!123"),
            dict(username='X', email="fb@eg.com", password1='foobar!123', password2='foobar!123'),
            dict(username='FooBar', email="", password1='foobar!123', password2='foobar!123'),
            dict(username='FooBar', email="fb@eg.com", password1='', password2='foobar!123'),
            dict(username='FooBar', email="fb@eg.com", password1='fb!12', password2='fb!12'),
            dict(username='FooBar', email="fb@eg.com", password1='foobar!12345', password2='foobar!123'),
            dict(username='Foo Bar', email="fb@eg.com", password1='foobar!123', password2='foobar!123'),
            dict(username='FooBar', email="foobar@example", password1='foobar!123', password2='foobar!123'),
            dict1,
        ]
        checks = [
            lambda h: self.assertIn('This field is required.', h),
            lambda h: self.assertIn(self.vldr_msgs['unm_l_rg'][:20], h),
            lambda h: self.assertIn('This field is required.', h),
            lambda h: self.assertIn('This field is required.', h),
            lambda h: self.assertIn(self.vldr_msgs['pw_l_rg'][:20], h),
            lambda h: self.assertIn(self.vldr_msgs['pw_match'], h),
            lambda h: self.assertIn(self.vldr_msgs['unm_no_wht_spc'], h),
            lambda h: self.assertIn(self.vldr_msgs['plz_val_em'], h),
            lambda h: self.assertIn(self.vldr_msgs['em_used'], h),
        ]
        # Tests
        for data, check in zip(datas, checks):
            with self.app.test_request_context():
                form = app_user.UserRegisterForm(data=data)
                resp = client.post("user/register", data=form.data, follow_redirects=True,)
                html = resp.data.decode()
                self.assertEqual(resp.status_code, 200)
                assert "Success" not in html, data
                check(html) #assertion

    def test_user_lifecycle(self):
        """Test processes of user registration, login, logout and deregistration.
        """
        client = self.app.test_client()
        # Register
        resp = client.get('user/register')
        self.assertEqual(resp.status_code, 200)
        # get string html data of webpage
        html = resp.data.decode()
        self.assertIn("Register", html)
        with self.app.test_request_context():
            form = app_user.UserRegisterForm(data=dict(
                username='Bobbylite',
                email='bob@example.com',
                password1='Password@1234',
                password2='Password@1234'
            ))
            resp = client.post("user/register", data=form.data, follow_redirects=True)
            html = resp.data.decode()
            self.assertEqual(resp.status_code, 200)
            assert 'Register' not in html, html
            assert 'Success' in html, html
        # Login
        with self.app.test_request_context():
            form = app_user.UserLoginForm(data=dict(
                username_email='Bobbylite',
                password='Password@1234',
            ))
            resp = client.post("user/login", data=form.data, follow_redirects=True)
            html = resp.data.decode()
            self.assertEqual(resp.status_code, 200)
            assert 'Login' not in html, html
            assert 'Logout' in html, html


class TestAdminUser(TestUser):

    def test_sign_in_out(self):
        """Ensure admin could sign in and out with correct privilages?"""
        client = self.app.test_client()

    def test_privileges(self):
        pass


if __name__ == "__main__":
    unittest.main()