from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


# Defining User model
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

    # Flask-Login required methods
    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

# Defining Post model
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

    # Relationships with other tables (User)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    replies = db.relationship('Reply', backref='post', cascade='all, delete-orphan', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.title or len(self.title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        if not self.content:
            raise ValueError("Content cannot be null")


# Defining Reply model
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    post_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)

    # Relationships with other tables (User, Post, and self)
    user = db.relationship('User', backref=db.backref('replies', lazy=True))
    parent_reply = db.relationship('Reply', remote_side=[id], backref=db.backref('child_replies', cascade='all, delete-orphan', lazy=True))

# Defining Task model, add record when user post.is_task is True
class Task(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True) # True: open, False: closed
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))

# Defining WaitingList model, add record when user apply for a task
class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
