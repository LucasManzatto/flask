from flask import request
from flask_restplus import Resource

from ..service.book_service import upsert_book, get_all_books, get_a_book, delete_book, get_book_author, get_book_genres
from ..util.dto import BookDTO

api = BookDTO.api
book_create = BookDTO.book_create
book_update = BookDTO.book_update
book_list = BookDTO.book_list
book_author = BookDTO.book_author
book_genres = BookDTO.book_genre


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(book_list, code=201, envelope='books')
    def get(self):
        """List all books."""
        return get_all_books()

    @api.expect(book_create)
    def post(self):
        """Creates a new book."""
        return upsert_book(request.json, update=False)

    @api.expect(book_update)
    def put(self):
        """Updates a book."""
        return upsert_book(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(book_list)
    def get(self, id):
        """Find a book by the ID."""
        return get_a_book(id)

    @staticmethod
    def delete(id):
        """Deletes a book."""
        return delete_book(id)


@api.route('/<int:id>/author/')
class BookAuthorItem(Resource):
    @api.marshal_with(book_author)
    def get(self, id):
        """Find the book's author."""
        return get_book_author(id)


@api.route('/<int:id>/genres/')
class BookGenreCollection(Resource):
    @api.marshal_with(book_genres)
    def get(self, id):
        """Find the book genres."""
        return get_book_genres(id)
