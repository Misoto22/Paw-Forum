from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    postcode = db.Column(db.String(10), nullable=True)
    join_at = db.Column(db.DateTime, default=datetime.utcnow)
    pet_type = db.Column(db.String(80), nullable=True)
    user_image = db.Column(db.String(255), nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    is_task = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, default=0)
    image_name = db.Column(db.String(100), nullable=True)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    replies = db.relationship('Reply', backref='post', cascade='all, delete-orphan', lazy=True)
    likes = db.relationship('PostLike', backref='post', cascade='all, delete-orphan', lazy=True)
    waiting_list_entries = db.relationship('WaitingList', backref='task_post', lazy=True, primaryjoin="and_(Post.id == WaitingList.task_id, Post.is_task == True)")

    @property
    def comment_count(self):
        return len(self.replies)

# Reply Model
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    post_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref=db.backref('replies', lazy=True))
    parent_reply = db.relationship('Reply', remote_side=[id], backref=db.backref('child_replies', cascade='all, delete-orphan', lazy=True))
    likes = db.relationship('ReplyLike', backref='reply', cascade='all, delete-orphan', lazy=True)

    @property
    def comment_count(self):
        return len(self.child_replies)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True)  # True: open, False: closed
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))

    post = db.relationship('Post', backref=db.backref('task', uselist=False))

# WaitingList Model
class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('waiting_list_entries', lazy=True))
    post = db.relationship('Post', primaryjoin="WaitingList.task_id == Post.id")

# PostLike Model
class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ReplyLike Model
class ReplyLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Activity Model
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    target_user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('activities', lazy=True))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
