from flask import request
from flask_restplus import Resource

from backend.src.main.service import author_service
from backend.src.main.util.dto import AuthorDTO
from webargs import fields
from webargs.flaskparser import use_args

api = AuthorDTO.api

author_args = {
    "query_all": fields.Str(missing=''),
    "id": fields.Str(missing=''),
    "name": fields.Str(missing='')
}


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_query, code=201)
    @use_args(author_args)
    def get(self, args):
        """List all authors."""
        return author_service.get_all_authors(args)

    @api.expect(AuthorDTO.author_create)
    def post(self):
        """Creates a new author."""
        return author_service.upsert_author(request.json, update=False)

    @api.expect(AuthorDTO.author_update)
    def put(self):
        """Updates an author."""
        return author_service.upsert_author(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(AuthorDTO.author_list)
    def get(self, id):
        """Find a author by the ID."""
        return author_service.get_an_author(id)

    @staticmethod
    def delete(id):
        """Deletes an author."""
        return author_service.delete_author(id)


@api.route('/<int:id>/books')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_books)
    def get(self, id):
        """Find the author books."""
        return author_service.get_author_books(id)


@api.route('/<int:id>/series')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_series)
    def get(self, id):
        """Find the author series."""
        return author_service.get_author_series(id)
