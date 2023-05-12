from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///'market.db'"
app.config['SECRET_KEY'] = '4599d342efd75b01713b4744'
db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)

from market import routes