from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    is_task = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, default=0)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    post_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)

class Task(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(100), nullable=True)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
