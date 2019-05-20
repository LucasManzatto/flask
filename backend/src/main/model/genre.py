from marshmallow import Schema, fields, post_load

from backend.src.main import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='genres', secondary='book_genres')

    def __init__(self, id=None, name=None, books=None):
        if books is None:
            books = []
        self.id = id
        self.name = name
        self.books = books

    def __repr__(self):
        return f"Genre-ID:{self.id},Name:{self.name}"


class GenreSchema(Schema):
    id = fields.Number(allow_none=True)
    name = fields.String(required=True)

    @post_load
    def make_genre(self, data):
        return Genre(**data)
