from flask import request
from flask_restplus import Resource

from backend.src.main.service.author_service import get_all_authors, upsert_author, get_an_author, delete_author, \
    get_author_books, get_author_series
from backend.src.main.util.dto import AuthorDTO

api = AuthorDTO.api


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_list, code=201, envelope='authors')
    def get(self):
        """List all authors."""
        return get_all_authors()

    @api.expect(AuthorDTO.author_create)
    def post(self):
        """Creates a new author."""
        return upsert_author(request.json, update=False)

    @api.expect(AuthorDTO.author_update)
    def put(self):
        """Updates an author."""
        return upsert_author(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(AuthorDTO.author_list)
    def get(self, id):
        """Find a author by the ID."""
        return get_an_author(id)

    @staticmethod
    def delete(id):
        """Deletes an author."""
        return delete_author(id)


@api.route('/<int:id>/books')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_books)
    def get(self, id):
        """Find the author books."""
        return get_author_books(id)


@api.route('/<int:id>/series')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_series)
    def get(self, id):
        """Find the author series."""
        return get_author_series(id)
