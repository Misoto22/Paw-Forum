import os
baseurl = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseurl, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AVATAR_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'avatar', 'uploads')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'image', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}