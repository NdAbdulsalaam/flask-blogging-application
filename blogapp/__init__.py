from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets

secret_key = secrets.token_hex(24)

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
# db.app = app
bcrypt = Bcrypt(app)

# These imports should always be below
from blogapp import routes

from blogapp.models import User, Post
with app.app_context():
    db.create_all()