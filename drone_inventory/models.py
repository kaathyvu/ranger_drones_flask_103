from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from flask_marshmallow import Marshmallow


# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash
# ^ This basically hashes our password in our database

# Import for Secrets -- Creates a user token by using a function called token hex which randomly generates a token
import secrets

# Timestamp for User Creation
from datetime import datetime

# Flask login to check for an authenicated user
from flask_login import UserMixin, LoginManager

db = SQLAlchemy() # This instantiates our db. Don't forget parentheses
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    # If user doesn't provide a first name or last name, then it can be null and the default will be an empty string
    email = db.Column(db.String(150), nullable=False)
    # Email will not be able to be null, because the user's email will be the login
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True) # a token ties one user to their drone collection (many drones)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True)

    # TO DO: add a backref relationship to the drone table

    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24) # this sets a token that is 24 char long
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
        # The uuid.uuid4() generates a random UUID

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    camera_quality = db.Column(db.String(150), nullable=True)
    flight_time = db.Column(db.String(100), nullable=True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f"The following drone has been added: {self.name}"

    def set_id(self):
        return secrets.token_urlsafe() # creates an id token hex


class DroneSchema(ma.Schema): #ma.Schema is pulling in our marshmallow object and our Schema in our instance of marshmallow
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_production', 'series']

drone_schema = DroneSchema()
drones_schema = DroneSchema(many=True)