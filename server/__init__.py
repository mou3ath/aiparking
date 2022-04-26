import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
secret_key = secrets.token_hex(16)
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginManager= LoginManager(app)
loginManager.login_view = 'login'
from server import routes