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
    return redirect('/users')

@app.get('/users')
def show_users():
    user_list = User.query.all()
    return render_template('users.html', users=user_list)

@app.get('/users/new')
def show_add_user_page():
    return render_template('addUser.html')

@app.post('/users/new')
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    user = User.query.get(user_id)
    return render_template('userPage.html', user=user)