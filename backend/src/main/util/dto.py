from flask_restplus import fields

from backend.src.main import api


class BookDTO:
    api = api.namespace('books', description='Operations related to books')

    book = api.model('Book', {
        'id': fields.String(readOnly=True, description='The ID of the book.'),
        'title': fields.String(readOnly=True, description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.')
    })
