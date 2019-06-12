from flask import request
from flask_restplus import Resource

from backend.src.main.service.author_service import AuthorService
from backend.src.main.util.dto import AuthorDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = AuthorDTO.api

author_args = {
    "id": fields.Str(missing=''),
    "name": fields.Str(missing='')
}
author_args.update(base_args)

author_service = AuthorService()


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
class AuthorCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_query, code=201)
    @use_args(author_args)
    def get(self, args):
        """List all authors."""
        return author_service.get_all(args)

    @api.expect(AuthorDTO.author_create)
    def post(self):
        """Creates a new author."""
        return author_service.upsert(request.json, update=False)

    @api.expect(AuthorDTO.author_update)
    def put(self):
        """Updates an author."""
        return author_service.upsert(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @api.marshal_with(AuthorDTO.author_list)
    def get(self, id):
        """Find a author by the ID."""
        return author_service.get_one(id)

    @staticmethod
    def delete(id):
        """Deletes an author."""
        return author_service.delete(id)


@api.route('/<int:id>/books')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_books)
    def get(self, id):
        """Find the author books."""
        return author_service.get_model_fk(id, 'books')


@api.route('/<int:id>/series')
class BookCollection(Resource):
    @api.marshal_list_with(AuthorDTO.author_series)
    def get(self, id):
        """Find the author series."""
        return author_service.get_model_fk(id, 'series')
