from flask import request
from flask_restplus import Resource
from main.service.author_service import get_all_authors, create_author, update_author, get_an_author, delete_author

from ..util.dto import AuthorDTO

api = AuthorDTO.api
author_list = AuthorDTO.author_list
author_create = AuthorDTO.author_create


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(author_list, code=201, envelope='authors')
    def get(self):
        """List all authors."""
        return get_all_authors()

    @api.response(201, 'Author successfully created.')
    @api.expect(author_create)
    def post(self):
        """Creates a new author."""
        return create_author(request.json)

    @api.response(201, 'Author successfully updated.')
    @api.expect(author_create)
    def put(self):
        """Updates an author."""
        return update_author(request.json)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(author_list)
    def get(self, id):
        """Find a author by the ID."""
        return get_an_author(id)

    @api.response(201, 'Atuhor successfully deleted.')
    def delete(self, id):
        """Deletes an author."""
        return delete_author(id)
