# to run test
# python3 -m unittest test_models.py
from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    # def test_greet(self):
        # user = User(f_name="UserTest", l_name="lastnameuser")
        # self.assertEquals(user.greet(), "I'm TestPet the dog")

    # def test_feed(self):
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
