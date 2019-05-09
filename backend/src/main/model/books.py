from backend.src.main import db
from marshmallow import post_load, Schema, fields


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', name='fk_book_author'), nullable=True)
    author = db.relationship("Author", back_populates='books')
    series_id = db.Column(db.Integer, db.ForeignKey('series.id', name='fk_book_series'),
                          nullable=True)
    series = db.relationship("Series", back_populates='books')

    def __init__(self, title, description, author_id=0):
        self.title = title
        self.description = description
        self.author_id = author_id

    def __repr__(self):
        return f"Book:{self.title} , Author ID:{self.author_id}"


class BookSchema(Schema):
    description = fields.String()
    title = fields.String()
    author_id = fields.Number()

    @post_load
    def make_book(self, data):
        return Book(**data)

# class BookSchema(ModelSchema):
#     class Meta:
#         model: Book
#         sqla_session = db.session
#         transient = True
