from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Step 1: Setting Up the Flask Application
app = Flask(__name__)

# Set up the database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Step 2: Defining Database Models
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    suburb = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postcode = db.Column(db.String(10))
    join_at = db.Column(db.DateTime, default=datetime)


class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    is_task = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)
    content = db.Column(db.Text)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    post_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    content = db.Column(db.Text)
    post_at = db.Column(db.DateTime, default=datetime)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, db.ForeignKey('threads.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))


class UserActivity(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(100))
    update_at = db.Column(db.DateTime, default=datetime)


class UserStatus(db.Model):
    __tablename__ = 'userstatuses'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    is_online = db.Column(db.Boolean, nullable=False)


class WaitingList(db.Model):
    __tablename__ = 'waitinglist'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime)


# Step 3: Creating the Database
if __name__ == '__main__':
    db.create_all()  # Creates the database and tables
    app.run(debug=True)
