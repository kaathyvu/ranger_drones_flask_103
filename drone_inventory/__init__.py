from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from config import Config # this goes into our config.py and grabs our Config class
from flask_migrate import Migrate # this connects our application to sqlalchemy
from .models import db as root_db, login_manager, ma
from drone_inventory.helpers import JSONEncoder

# Flask Cors Import -- Cross origin resource sharing -- future proofing from an external source
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app) # Instantiates our database in our application
migrate = Migrate(app, root_db)

login_manager.init_app(app) 
login_manager.login_view = 'auth.signin' 

ma.init_app(app)
app.json_encoder = JSONEncoder

CORS(app)