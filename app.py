"""Blogly application."""
# run development mode with
# FLASK_DEBUG=1 flask run
# FLASK_ENV deprecated
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "FlaskAndSQLareBeast"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
# db.drop_all()
# db.create_all()

# debug app tool
debug = DebugToolbarExtension(app)
# GET /


@app.route("/")
def home():
    """ Home route """
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    f_date = [post.created_at.strftime('%c') for post in posts]
    return render_template("index.html", posts=posts, dates=f_date)
# GET /users


@app.route("/users")
def get_users():
    """ Get all users """
    users = User.query.all()
    return render_template("users.html", users=users)

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
    """ User Edit route """
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

# POST /users/[user-id]/edit


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """ Update User information """
    user = User.query.get_or_404(user_id)
    user.f_name = request.form["first-name"].capitalize()
    user.l_name = request.form["last-name"].capitalize()
    user.img_url = request.form["img-url"]
    db.session.commit()
    # updated successful message
    flash("Updated successful", "success")
    return redirect(f"/{user_id}")


# POST /users/[user-id]/delete

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Delete user profile """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    # deletion successful message, error is just for styling purpose
    flash("User deleted", "error")
    return redirect("/")


# GET /users/[user-id]/posts/new
# Show form to add a post for that user.

# ************* post branch *************
# ***************************************
@app.route("/users/<int:user_id>/posts/new")
def get_add_post_form(user_id):
    """ Add post form route """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("add-post.html", user=user, tags=tags)


# POST /users/[user-id]/posts/new
# Handle add form; add post and redirect to the user detail page.
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """ Add Post route """
    user = User.query.get_or_404(user_id)
    title = request.form["title"].capitalize()
    content = request.form["content"].capitalize()
    tag_ids = [int(tag_id) for tag_id in request.form.getlist('post-tags')]
    tags_list = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # create a post with current time
    post = Post(title=title, content=content,
                created_at=datetime.now(), user_id=user.id, tags=tags_list)
    db.session.add(post)
    db.session.commit()

    # Created post successful message
    flash("Created Post", "success")
    return redirect(f"/{user.id}")

# GET /posts/[post-id]
# Show a post.
# Show buttons to edit and delete the post.


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """ Render user post """
    post = Post.query.get_or_404(post_id)
    f_date = post.created_at.strftime('%c')
    return render_template("posts.html", post=post, date=f_date)

# GET /posts/[post-id]/edit
# Show form to edit a post, and to cancel (back to user page).


@app.route("/posts/<int:post_id>/edit")
def get_post_edit_form(post_id):
    """ Edit form route """
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()
    print(post.tags)
    return render_template("/edit-post.html", post=post, all_tags=all_tags)

# POST /posts/[post-id]/edit
# Handle editing of a post. Redirect back to the post view.


@app.route("/post/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """ Update post """
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    # handle new tags for post
    post.tags.clear()
    post.tags = Tag.query.filter(
        Tag.id.in_(request.form.getlist('post-tags'))).all()
    # update post
    db.session.commit()
    # Post updated success message
    flash("Post updated", "success")
    return redirect(f"/{post.users.id}")

# POST /posts/[post-id]/delete
# Delete the post.


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ Delete post """
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    # Deleted successful, error is just for styling purpose
    flash("Post deleted", "error")
    return redirect(f"/{post.user_id}")

# ***************************************
# *************** Tags ******************
# ***************************************

# GET /tags
# Lists all tags, with links to the tag detail page.


@app.route("/tags")
def tags():
    """ Route with all tags """
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

# GET /tags/[tag-id]
# Show detail about a tag. Have links to edit form and to delete.


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """ Show tag with posts """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-details.html", tag=tag)

# GET /tags/new
# Shows a form to add a new tag.


@app.route("/tags/new")
def get_new_tag_form():
    """ Get tag form """
    return render_template("add-tag.html")

# POST /tags/new
# Process add form, adds tag, and redirect to tag list.


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """ Add created tag """
    created_tag = request.form["tag-name"]
    tag = Tag(tag_name=created_tag)
    db.session.add(tag)
    db.session.commit()
    flash("Tag created", "success")
    return redirect("/tags")

# GET /tags/[tag-id]/edit
# Show edit form for a tag.


@app.route("/tags/<int:tag_id>/edit")
def get_edit_tag_form(tag_id):
    """ Edit tag form """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit-tag.html", tag=tag)

# POST /tags/[tag-id]/edit
# Process edit form, edit tag, and redirects to the tags list.


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """ Edit tag """
    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form["tag-name"]
    db.session.commit()
    flash("Tag updated", "success")
    return redirect(f"/tags")

# POST /tags/[tag-id]/delete
# Delete a tag.


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Delete tag """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    # tag removed successful
    flash("Tag removed", "error")
    return redirect("/tags")

# To DO
# tag details show post assocciated with that tag
