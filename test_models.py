# to run test
# SQLALCHEMY_WARN_20=1 python3 -m unittest test_models.py
from unittest import TestCase

from app import app
from models import db, User, Post


class UserModelTestCase(TestCase):
    """ Tests Users model """

    def setUp(self):
        """Clean up any existing users."""
        self.client = app.test_client()
        # use test database
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_DATABASE_URI": "postgresql:///blogly_test",
            "DEBUG_TB_HOSTS": ["dont-show-debug-toolbar"]
        })
        with app.app_context():
            self.ids = []  # will hold users ids

            db.drop_all()
            db.create_all()
            user = User(f_name="west",
                        l_name="east", img_url="number1")
            user2 = User(f_name="west",
                         l_name="east", img_url="number1")
            db.session.add_all([user, user2])
            # commit to test database
            db.session.commit()

            # append user ids
            self.ids.append(user.id)
            self.ids.append(user2.id)

            # add tester post
            post = Post(title="hello", content="world",
                        created_at="2021-04-20 09:22:00", user_id=self.ids[0])
            post1 = Post(title="hello", content="world",
                         created_at="2020-04-20 10:22:00", user_id=self.ids[0])
            db.session.add_all([post, post1])
            db.session.commit()
            self.p_title = post.title
            # delete post first
            Post.query.delete()
            # delete Users last
            User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    # *******************************************
    # *************** User test *****************
    # *******************************************
    def test_greet(self):
        """ Test User greet method """
        user = User(f_name="Ed", l_name="Aviles")

        self.assertEqual(
            user.greet(), f"Hi my name is {user.f_name} {user.l_name}!")

    def test_get_all_users_by_first_name(self):
        """ Test class method get_all_users_by_first_name """
        with app.app_context():
            # get all users form test database
            users = User.query.all()
            # get all users using User class method
            users_list = User.get_all_users_by_first_name(users[0].f_name)
        self.assertEqual(users, users_list)

    def test_get_all_users_by_last_name(self):
        """ Test class method get_all_users_by_last_name """
        with app.app_context():
            # get all users form test database
            users = User.query.all()
            # get all users using User class method
            users_list = User.get_all_users_by_last_name(users[0].l_name)
        self.assertEqual(users, users_list)

    def test_get_all_users_by_default_image_url(self):
        """ Test class method get_all_users_by_default_image_url """
        with app.app_context():
            # get all users form test database
            users = User.query.all()
            # get all users using User class method
            users_list = User.get_all_users_by_default_image_url(
                users[0].img_url)
        self.assertEqual(users, users_list)

    # *******************************************
    # *************** Post test *****************
    # *******************************************
    def test_get_all_posts_by_user(self):
        """ Test for all posts by user """
        with app.app_context():
            posts = Post.get_all_posts_by_user(self.ids[0])
        # should only be 2 posts by user with id 1
        self.assertEqual(2, len(posts))

    def test_get_all_posts_by_title(self):
        """ Test getting all posts by title """
        with app.app_context():
            posts = Post.get_all_posts_by_title(self.p_title)
        # should be 2 posts with the same title
        self.assertEqual(len(posts), 2)
