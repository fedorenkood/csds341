import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(32)
    # app.config['SECRET_KEY'] = SECRET_KEY
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mysql://csds341:admin@127.0.0.1/csds341_questionnaire"
    SQLALCHEMY_TRACK_MODIFICATIONS = False