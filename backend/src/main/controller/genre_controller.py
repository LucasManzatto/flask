from flask import request
from flask_restplus import Resource
from backend.src.main.service import genre_service

from backend.src.main.util.dto import GenreDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = GenreDTO.api

genre_args = {
    "query_all": fields.Str(missing=''),
    "id": fields.Str(missing=''),
    "name": fields.Str(missing='')
}
genre_args.update(base_args)


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Genre not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(GenreDTO.genre_query, code=201)
    @use_args(genre_args)
    def get(self, args):
        """List all genres."""
        return genre_service.get_all_genres(args)

    @api.expect(GenreDTO.genre_create)
    def post(self):
        """Creates a new genre."""
        return genre_service.upsert_genre(request.json, update=False)

    @api.expect(GenreDTO.genre_update)
    def put(self):
        """Updates a genre."""
        return genre_service.upsert_genre(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @staticmethod
    @api.marshal_with(GenreDTO.genre_list)
    def get(id):
        """Find a genre by the ID."""
        return genre_service.get_a_genre(id)

    @staticmethod
    def delete(id):
        """Deletes a genre."""
        return genre_service.delete_genre(id)


@api.route('/<int:id>/books')
class GenreBookCollection(Resource):
    @api.marshal_with(GenreDTO.genre_books)
    def get(self, id):
        """Find the genre books."""
        return genre_service.get_genre_books(id)
