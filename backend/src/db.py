from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
app = Flask(__name__)
api.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
