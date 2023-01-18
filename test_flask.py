# to run test
# SQLALCHEMY_WARN_20=1 python3 -m unittest test_flask.py
from unittest import TestCase

from app import app
from models import db, User

# Use test database and not app SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
# app.config['SQLALCHEMY_ECHO'] = False
# Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True
# This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User."""
        self.client = app.test_client()
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_DATABASE_URI": "postgresql:///blogly_test",
            "DEBUG_TB_HOSTS": ["dont-show-debug-toolbar"]
        })
        # create an app context
        with app.app_context():
            db.drop_all()
            db.create_all()

            User.query.delete()

            user = User(f_name="first_name_test",
                        l_name="last_name_test", img_url="testurl")

            db.session.add(user)
            db.session.commit()
            # db.session.commit() will return user.id
            self.user_id = user.id
            self.f_name = user.f_name
            self.l_name = user.l_name
            self.img_url = user.img_url

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        """ Test Home route """
        with self.client:
            # will redirect route
            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 302)
            # allow redirect
            resp = self.client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn(
                f'<li><a href="/1"">{self.f_name}&nbsp;{self.l_name}</a>', html)

    def test_show_user(self):
        """ Test getting a User by id route"""
        with self.client:
            # get user with certain id
            resp = self.client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # check if user is displayed
            self.assertIn(
                f'<div class="user-name">{self.f_name}&nbsp;{self.l_name}</div>', html)
            # check if Edit button is displayed
            self.assertIn(
                '<a class="btn btn-edit" href="/users/1/edit">Edit</a>', html)
            # check if Delete button is displayed
            self.assertIn(
                '<a class="btn btn-delete" href="/users/1/delete">Delete</a>', html)

    def test_add_user(self):
        """ Test adding a User """
        # with app.test_client() as client:
        with self.client:
            # create fake form data
            user_tester = {"first-name": "west",
                           "last-name": "east",
                           "img-url": "https://fakehost.com"}
            resp = self.client.post(
                "/users/new", data=user_tester, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<div class="user-name">{user_tester["first-name"]}&nbsp;{user_tester["last-name"]}</div>', html)

    def test_edit_user(self):
        """ Test edit route """
        with self.client:
            resp = self.client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            print(html)
            self.assertIn(f"<h1>Edit {self.f_name}'s Profile</h1>", html)
