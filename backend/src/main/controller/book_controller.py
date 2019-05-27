from flask import request
from flask_restplus import Resource

from backend.src.main.service import book_service
from backend.src.main.util.dto import BookDTO
from webargs import fields
from webargs.flaskparser import use_args

api = BookDTO.api

books_args = {
    "query_all": fields.Str(missing=''),
    "id": fields.Str(missing=''),
    "title": fields.Str(missing=''),
    "description": fields.Str(missing=''),
    'author': fields.Str(missing='')
}


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):

    @api.marshal_list_with(BookDTO.book_query, code=201)
    @use_args(books_args)
    def get(self, args):
        """List all books."""
        return book_service.get_all_books(args)

    @api.expect(BookDTO.book_create)
    def post(self):
        """Creates a new book."""
        return book_service.upsert_book(request.json, update=False)

    @api.expect(BookDTO.book_update)
    def put(self):
        """Updates a book."""
        return book_service.upsert_book(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(BookDTO.book_list)
    def get(self, id):
        """Find a book by the ID."""
        return book_service.get_a_book(id)

    @staticmethod
    def delete(id):
        """Deletes a book."""
        return book_service.delete_book(id)


@api.route('/<int:id>/author')
class BookAuthorItem(Resource):
    @api.marshal_with(BookDTO.book_author)
    def get(self, id):
        """Find the book's author."""
        return book_service.get_book_author(id)


@api.route('/<int:id>/genres')
class BookGenreCollection(Resource):
    @api.marshal_with(BookDTO.book_genre)
    def get(self, id):
        """Find the book genres."""
        return book_service.get_book_genres(id)


@api.route('/<int:id>/series')
class BookSeriesItem(Resource):
    @api.marshal_with(BookDTO.book_series)
    def get(self, id):
        """Find the book series."""
        return book_service.get_book_series(id)
