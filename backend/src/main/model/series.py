from backend.src.main import db
from main.model.author import author_series
from marshmallow import post_load, Schema, fields


class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))
    books = db.relationship("Book", back_populates='series')
    authors = db.relationship("Author", back_populates='series', secondary=author_series)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Series:{self.title}"


class SeriesSchema(Schema):
    description = fields.String()
    title = fields.String()

    @post_load
    def make_series(self, data):
        return Series(**data)