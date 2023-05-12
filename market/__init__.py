from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///'market.db'"
app.config['SECRET_KEY'] = '4599d342efd75b01713b4744'
db = SQLAlchemy()
db.init_app(app)

from market import routes