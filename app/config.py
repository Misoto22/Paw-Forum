import os
baseurl = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'verysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseurl, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
