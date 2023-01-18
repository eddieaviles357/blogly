# to run test
# SQLALCHEMY_WARN_20=1 python3 -m unittest test_models.py
from unittest import TestCase

from app import app
from models import db, User


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
            user = User(f_name="first_name_test",
                        l_name="last_name_test", img_url="testurl")
            user2 = User(f_name="first_name_test",
                         l_name="last_name_test", img_url="testurl")
            db.session.add(user)
            db.session.add(user2)
            # commit to test database
            db.session.commit()
            # append user ids
            self.ids.append(user.id)
            self.ids.append(user2.id)
            # delete Users
            User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_greet(self):
        user = User(f_name="Ed", l_name="Aviles")

        self.assertEqual(
            user.greet(), f"Hi my name is {user.f_name} {user.l_name}!")

    def test_get_all_users_by_first_name(self):
        with app.app_context():
            # get all users form test database
            users = User.query.all()
            # get all users using User class method
            users_list = User.get_all_users_by_first_name(users[0].f_name)
            self.assertEqual(users, users_list)
