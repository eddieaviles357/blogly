"""Blogly application."""
# run development mode with
# FLASK_DEBUG=1 flask run
# FLASK_ENV deprecated
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "FlaskAndSQLareBeast"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
# db.create_all()

# debug app tool
debug = DebugToolbarExtension(app)

# GET /


@app.route("/")
def home():
    """ Home route """
    return redirect("/users")

# GET /users


@app.route("/users")
def get_users():
    """ Get all users """
    users = User.query.all()
    return render_template("index.html", users=users)

# GET /users/new


@app.route("/users/new")
def add_user():
    """ Create new user route """
    return render_template("add-user.html")

# POST /users/new


@app.route("/users/new", methods=["POST"])
def create_user():
    """ Created User route """
    first_n = request.form["first-name"]
    last_n = request.form["last-name"]
    # if img-url was left empty assign default img-url
    img = request.form["img-url"]
    img = img if img else None

    # create user object
    user = User(f_name=first_n, l_name=last_n, img_url=img)

    db.session.add(user)  # add user to session
    db.session.commit()  # commit to database
    # Created successful message
    flash("Created User", "success")
    return redirect(f"/{user.id}")

# GET /users/[user-id]


@app.route("/<int:user_id>")
def show_users(user_id):
    """Show user details """

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

# GET /users/[user-id]/edit


@app.route("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """ Edit user form route """
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

# POST /users/[user-id]/edit


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.f_name = request.form["first-name"]
    user.l_name = request.form["last-name"]
    user.img_url = request.form["img-url"]
    db.session.commit()
    # updated successful message
    flash("Updated successful", "success")
    return redirect(f"/{user_id}")


# POST /users/[user-id]/delete


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Delete user profile """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    # deletion successful message
    flash("Deleted User", "error")
    return redirect("/")
