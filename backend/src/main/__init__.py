from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
api = Api()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    api.init_app(app)
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
