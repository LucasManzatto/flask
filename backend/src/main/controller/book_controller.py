from flask import request
from flask_restplus import Resource

from ..service.book_service import upsert_book, get_all_books, get_a_book, delete_book, get_book_author
from ..util.dto import BookDTO, AuthorDTO

api = BookDTO.api
book_create = BookDTO.book_create
book_update = BookDTO.book_update
book_list = BookDTO.book_list
author_list = AuthorDTO.author_list


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


@api.route('/<int:book_id>')
class BookItem(Resource):
    @staticmethod
    @api.marshal_with(book_list)
    def get(book_id):
        """Find a book by the ID."""
        return get_a_book(book_id)

    @staticmethod
    def delete(book_id):
        """Deletes a book."""
        return delete_book(book_id)


@api.route('/author/<int:id>')
class BookAuthorItem(Resource):
    @api.marshal_with(author_list)
    def get(self, id):
        """Find the book's author."""
        return get_book_author(id)
