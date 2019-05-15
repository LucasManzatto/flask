from flask import request
from flask_restplus import Resource
from main.service.author_service import get_all_authors, upsert_author, get_an_author, delete_author

from ..util.dto import AuthorDTO

api = AuthorDTO.api
author_list = AuthorDTO.author_list
author_create = AuthorDTO.author_create
author_update = AuthorDTO.author_update


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(author_list, code=201, envelope='authors')
    def get(self):
        """List all authors."""
        return get_all_authors()

    @api.expect(author_create)
    def post(self):
        """Creates a new author."""
        return upsert_author(request.json, update=False)

    @api.expect(author_update)
    def put(self):
        """Updates an author."""
        return upsert_author(request.json, update=True)


@api.route('/<int:author_id>')
class BookItem(Resource):
    @api.marshal_with(author_list)
    def get(self, author_id):
        """Find a author by the ID."""
        return get_an_author(author_id)

    @staticmethod
    def delete(author_id):
        """Deletes an author."""
        return delete_author(author_id)
