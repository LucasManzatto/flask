from backend.src.main import db
from marshmallow import Schema, fields, post_load


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='author')

    def __init__(self, name=None, books=[], id=0):
        self.id = id
        self.name = name
        self.books = books

    def __repr__(self):
        return f"Author-ID:{self.id},Name:{self.name}"


class AuthorSchema(Schema):
    id = fields.Number()
    name = fields.String()

    @post_load
    def make_author(self, data):
        return Author(**data)
