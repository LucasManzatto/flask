from marshmallow import Schema, fields, post_load
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

api = Api()
app = Flask(__name__)
api.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_updated_by = db.Column(db.String(30))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_updated_by = db.Column(db.String(30))
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))

    def __init__(self, title, description, last_updated_by):
        self.title = title
        self.description = description
        self.last_updated_by =last_updated_by

    def __repr__(self):
        return f"Book:{self.title}"


class BookSchema(Schema):
    id = fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.String()
    title = fields.String()
    description = fields.String()

    @post_load
    def make_book(self, data):
        return Book(**data)
