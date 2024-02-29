"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(30),
        nullable=False)

    last_name = db.Column(
        db.String(30),
        nullable=False)

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL)

# class Post(db.Model):
#     """Post."""

#     __tablename__ = "posts"

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True)

#     title = db.Column(
#         db.String(100),
#         nullable=False)

#     content = db.Column(
#         db.Text,
#         nullable=False)

#     created_at = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=db.func.now())

#     user_id = db.Column