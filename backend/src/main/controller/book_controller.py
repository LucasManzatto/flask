from flask import request
from flask_restplus import Resource

from ..service.book_service import create_book, get_all_books, get_a_book, delete_book, update_book, get_book_author
from ..util.dto import BookDTO, AuthorDTO

api = BookDTO.api
book_create = BookDTO.book_create
book_update = BookDTO.book_update
book_list = BookDTO.book_list
author_list = AuthorDTO.author_list


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(book_list, code=201, envelope='books')
    def get(self):
        """List all books."""
        return get_all_books()

    @api.response(201, 'Book successfully created.')
    @api.expect(book_create)
    def post(self):
        """Creates a new book."""
        return create_book(request.json)

    @api.response(201, 'Book successfully updated.')
    @api.expect(book_update)
    def put(self):
        """Updates a book."""
        return update_book(request.json)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(book_list)
    def get(self, id):
        """Find a book by the ID."""
        return get_a_book(id)

    @api.response(201, 'Book successfully deleted.')
    def delete(self, id):
        """Deletes a book."""
        return delete_book(id)


@api.route('/author/<int:id>')
class AuthorItem(Resource):
    @api.marshal_with(author_list)
    def get(self, id):
        """Find the book's author."""
        return get_book_author(id)
