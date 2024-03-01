"""Blogly application."""

import os

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def redirect_home():
    """Redirects to users page"""

    return redirect('/users')


@app.get('/users')
def show_users():
    """Shows users page"""

    user_list = User.query.order_by('last_name', 'first_name').all()
    return render_template('users.html', users=user_list)


@app.get('/users/new')
def show_add_user_page():
    """Show add user form"""

    return render_template('addUser.html')


@app.post('/users/new')
def create_user():
    """Adds new user to the database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url'] or None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows user info page"""

    user = User.query.get_or_404(user_id)
    return render_template('userPage.html', user=user)


@app.get('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Shows edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template('editUser.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Changes user data in the database"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url']

    db.session.commit()
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes user from database"""

    user = User.query.get_or_404(user_id)

    Post.query.filter_by(user_id = user.id).delete()
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def show_add_post_page(user_id):
    """Shows add post page"""

    user = User.query.get_or_404(user_id)
    return render_template('addPost.html', user = user)


@app.post('/users/<int:user_id>/posts/new')
def create_new_post(user_id):
    """Creates new post by the user"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


################################################################# Section 2 ##################################################
@app.get('/posts/<int:post_id>')
def show_post_page(post_id):
    """Shows a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('postPage.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form_page(post_id):
    """Shows edit post form page"""

    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)

@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edits the given post"""

    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()
    return redirect(f'/posts/{post.id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the given post"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')