from flask import request
from flask_restplus import Resource

from ..service.book_service import save_new_user, get_all_users, get_a_book, delete_book, update_book
from ..util.dto import BookDTO

api = BookDTO.api
_book = BookDTO.book


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(_book, code=201, envelope='books')
    def get(self):
        """List all books."""
        return get_all_users()

    @api.response(201, 'Book successfully created.')
    @api.expect(_book)
    def post(self):
        """Creates a new _book."""
        return save_new_user(request.json)

    @api.response(201, 'Book successfully updated.')
    @api.expect(_book)
    def put(self):
        """Updates a _book."""
        return update_book(request.json)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(_book)
    def get(self, id):
        """Find a _book by the ID."""
        return get_a_book(id)

    @api.response(201, 'Book successfully deleted.')
    def delete(self, id):
        """Deletes a _book."""
        return delete_book(id)
