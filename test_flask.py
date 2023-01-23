# to run test
# SQLALCHEMY_WARN_20=1 python3 -m unittest test_flask.py
from unittest import TestCase

from app import app
from models import db, User, Post

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
            post = Post(title="testing", content="content test",
                        created_at="2022-04-20 09:00:00", user_id=1)
            db.session.add(post)
            db.session.commit()
            p = Post(title="Wonderful", content="testing is needed",
                     created_at="2020-04-20 10:00:00", user_id=1)
            db.session.add(p)
            db.session.commit()
            # db.session.commit() will return user.id and post.id
            self.user_id = user.id
            self.f_name = user.f_name
            self.l_name = user.l_name
            self.img_url = user.img_url

            self.post_id = post.id
            self.title = post.title
            self.content = post.content
            self.created_at = post.created_at

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    # **********************************
    # *********** Users route **********
    # **********************************

    def test_list_users(self):
        """ Test Home route """
        with self.client:
            path = '/'
            # will redirect route
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 302)
            # allow redirect
            resp = self.client.get(path, follow_redirects=True)
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
                '<button class="btn btn-delete">Delete</button>', html)

    def test_add_user(self):
        """ Test adding a User """
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
            users = User.query.all()
            # User list should be increased by 1
            self.assertEqual(len(users), 2)

    def test_edit_user(self):
        """ Test edit route """
        with self.client:
            resp = self.client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # has users first name in header tag
            self.assertIn(f"<h1>Edit {self.f_name}'s Profile</h1>", html)

    # **************************************
    # ************** Post routes ***********
    # **************************************

    def test_get_add_post_form(self):
        """ Test for getting post form """
        with self.client:
            resp = self.client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # Add Post title from html
            self.assertIn("<title> Add Post </title>", html)
            # make sure users first and last name are displayed
            self.assertIn(
                f"<h1>Add Post for {self.f_name} {self.l_name}</h1>", html)

    def test_get_post(self):
        """ Test for getting post """
        with self.client:
            resp = self.client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # Has post title in title tag
            self.assertIn(f"<title> {self.title} </title>", html)
            # Has post content inside tag element
            self.assertIn(
                f'<div class="post-content">{self.content}</div>', html)

    def test_delete_post(self):
        """ Test for deleting a users post """
        with self.client:
            with app.app_context():
                posts = Post.query.all()
            path = f"/posts/{self.post_id}/delete"
            # should have 2 post
            self.assertEqual(len(posts), 2)
            # once we hit route user post should be decreased by 1
            resp = self.client.post(path, follow_redirects=True)
            html = resp.get_data(as_text=True)
            # update posts
            posts = Post.query.all()
            self.assertEqual(resp.status_code, 200)
            # post length should be decreased by one
            self.assertEqual(len(posts), 1)
