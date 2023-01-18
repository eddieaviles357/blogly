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
            db.drop_all()
            db.create_all()

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
        # user = User(f_name="UserTest", l_name="lastnameuser")
        # user.feed(5)
        # self.assertEquals(user.hunger, 5)

        # user.feed(999)
        # self.assertEquals(user.hunger, 0)

        # def test_get_by_species(self):
        #     user = User(f_name="UserTest", l_name="lastnameuser")
        #     db.session.add(user)
        #     db.session.commit()

        # dogs = User.get_by_species('dog')
        # self.assertEquals(dogs, [user])
