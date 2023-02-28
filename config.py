import os

class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cannot-be-guess'
    
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@127.0.0.2:5433/store"
    SQLALCHEMY_TRACK_MODIFICATIONS = False