from flask_restplus import fields

from backend.src.main import api


class AuthorDTO:
    api = api.namespace('authors', description='Operations related to authors.')

    author_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    author_create = api.model("Author_Create", {
        'id': fields.Integer(description='The ID of the book.'),
        'name': fields.String(description='The name of the author.')
    })

    author_list = api.model('Author_List', {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
        'books': fields.Nested(author_books)
    })


class BookDTO:
    api = api.namespace('books', description='Operations related to books')

    book_author = api.model('Book_Author', {
        'id': fields.String(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
    })

    book_create = api.model('Book_Create', {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(required=True, description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
        'author_id': fields.Integer(required=False, description="The book's author.")
    })

    book_list = api.model('Book_List', {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
        'author': fields.Nested(book_author)
    })


class SeriesDTO:
    api = api.namespace('series', description='Operations related to series.')

    series_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    series_create = api.model('Series_Create', {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.'),
        'books_ids': fields.List(fields.Integer(required=False, description="The series's books."))
    })

    series_list = api.model('Series_List', {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.'),
        'books': fields.Nested(series_books)
    })


class MLDTO:
    api = api.namespace('predict', description='Operations related to machine learning.')

    data = api.model('Data_List', {
        'data': fields.List(fields.Integer(required=False))
    })
