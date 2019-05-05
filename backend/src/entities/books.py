import datetime

from marshmallow import post_load
from marshmallow_sqlalchemy import TableSchema

from backend.src.db import db
from backend.src.entities.entity import Entity


class Book(Entity, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))

    def __init__(self, title, description, updated_at, last_updated_by='Script', created_at=datetime.datetime.now()):
        self.title = title
        self.description = description
        self.last_updated_by = last_updated_by
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"Book:{self.title}"


class BookSchema(TableSchema):
    class Meta:
        table: Book

    @post_load
    def make_book(self, data):
        return Book(**data)
