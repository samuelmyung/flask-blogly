"""Blogly application."""

import os

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

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

    user_list = User.query.all().order_by('last_name', 'first_name')
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

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
