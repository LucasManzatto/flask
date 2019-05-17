from backend.src.main import db
from marshmallow import Schema, fields, post_load, INCLUDE

author_series = db.Table('author_series', db.Model.metadata,
                         db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                         db.Column('series_id', db.Integer, db.ForeignKey('series.id'))
                         )


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='author')
    series = db.relationship("Series", back_populates='authors', secondary=author_series)

    def __init__(self, id=None, name=None, books=None):
        if books is None:
            books = []
        self.id = id
        self.name = name
        self.books = books

    def __repr__(self):
        return f"Author-ID:{self.id},Name:{self.name}"


class AuthorSchema(Schema):
    id = fields.Number()
    name = fields.String(required=True)

    @post_load
    def make_author(self, data):
        return Author(**data)
