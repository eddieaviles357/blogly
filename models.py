"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://images.unsplash.com/photo-1614436163996-25cee5f54290?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1042&q=80'


def connect_db(app):
    """ Connect to Database """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15), nullable=False)
    img_url = db.Column(db.String(
        200), default=DEFAULT_IMG_URL)

    def __repr__(self):
        """ User representation """
        return f"<User {self.id} {self.f_name} {self.l_name} {self.img_url}>"

    def greet(self):
        """ Greet user name and last name """
        return f"Hi my name is {self.f_name} {self.l_name}!"

    @classmethod
    def get_all_users_by_first_name(cls, f_name):
        """ Get all users from database that match first_name """
        return cls.query.filter_by(f_name=f_name).all()

    @classmethod
    def get_all_users_by_last_name(cls, l_name):
        """ Get all users from database that match last_name """
        return cls.query.filter_by(l_name=l_name).all()

    @classmethod
    def get_all_users_by_default_image_url(cls, img_url):
        """ Get all users from database that match default image URL  """
        return cls.query.filter_by(img_url=img_url).all()
