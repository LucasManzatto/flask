from flask_restplus import fields

from backend.src.main import api


class AuthorDTO:
    api = api.namespace('authors', description='Operations related to authors.')

    author_base = api.model("Author_Base", {
        'name': fields.String(description='The name of the author.'),
    })

    author_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    author_series = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.')
    })

    author_create = api.clone("Author_Create", author_base, {
        'series_ids': fields.List(fields.Integer(required=False, description="The author's series."))
    })

    author_update = api.clone('Author_Clone', author_create, {
        'id': fields.Integer(description='The ID of the book.'),
    })

    author_list = api.model('Author_List', {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
        'books': fields.Nested(author_books),
        'series': fields.Nested(author_series)
    })


class BookDTO:
    api = api.namespace('books', description='Operations related to books')

    book_base = api.model('Book_Base', {
        'title': fields.String(required=True, description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    book_author = api.model('Book_Author', {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
    })
    book_series = api.model('Book_Series', {
        'id': fields.Integer(description='The ID of the series.'),
        'title': fields.String(description='The name of the series.'),
        'description': fields.String(description='The description of the series.'),
    })

    book_create = api.clone('Book_Update', book_base, {
        'author_id': fields.Integer(required=False, description="The book's author."),
        'series_id': fields.Integer(required=False, description="The book's series.")
    })

    book_update = api.clone('Book_Create', book_create, {
        'id': fields.Integer(description='The ID of the book.'),
    })

    book_list = api.clone('Book_List', book_base, {
        'id': fields.Integer(description='The ID of the book.'),
        'author': fields.Nested(book_author),
        'series': fields.Nested(book_series)
    })


class SeriesDTO:
    api = api.namespace('series', description='Operations related to series.')

    series_base = api.model('Series_Base', {
        'title': fields.String(required=True, description='The title of the series.'),
        'description': fields.String(required=True, description='The description of the series.'),
    })

    series_books = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the book.'),
        'title': fields.String(description='The title of the book.'),
        'description': fields.String(required=True, description='The description of the book.'),
    })

    series_authors = api.model("Author_Books", {
        'id': fields.Integer(description='The ID of the author.'),
        'name': fields.String(description='The name of the author.'),
    })

    series_create = api.clone('Series_Create', series_base, {
        'books_ids': fields.List(fields.Integer(required=False, description="The series's books."))
    })

    series_update = api.clone('Series_Update', series_create, {
        'id': fields.Integer(description='The ID of the series.'),
    })

    series_list = api.clone('Series_List', series_base, {
        'id': fields.Integer(description='The ID of the series.'),
        'books': fields.Nested(series_books),
        'authors': fields.Nested(series_authors)
    })
