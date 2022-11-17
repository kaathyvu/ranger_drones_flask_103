import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Sets our basedir variable to be able to find the absolute path of our config.py file
# Therefore we can access this file on any Operating System (OS)
# Allows outside file/folders to be added to the project from the base directory

load_dotenv(os.path.join(basedir, '.env'))
# This allows us to run everything without setting up the flask app every time

class Config():
    """
    Set config variable for the flask app
    Using environment variables where available
    Otherwise create the config variable if not done already

    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Nana nana boo boo youll never guess!'
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Note spelling above, it is supposed to be URI, then URL!
    # If it cannot connect to the database, it will connect to sqlite which is a temporary local storage (which is not ideal)
    # If it connects to sqlite, make sure there are no typos!
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This turns off updates from SQLAlchemy which makes debugging look less cluttered