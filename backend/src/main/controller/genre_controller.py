from flask import request
from flask_restplus import Resource
from backend.src.main.service import genre_service

from backend.src.main.util.dto import GenreDTO

api = GenreDTO.api
genre_create = GenreDTO.genre_create
genre_update = GenreDTO.genre_update
genre_list = GenreDTO.genre_list
genre_books_list = GenreDTO.genre_books


@api.route('/')
@api.doc(
    responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Genre not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @api.marshal_list_with(genre_list, code=201)
    def get(self):
        """List all genres."""
        return genre_service.get_all_genres()

    @api.expect(genre_create)
    def post(self):
        """Creates a new genre."""
        return genre_service.upsert_genre(request.json, update=False)

    @api.expect(genre_update)
    def put(self):
        """Updates a genre."""
        return genre_service.upsert_genre(request.json, update=True)


@api.route('/<int:id>')
class BookItem(Resource):
    @staticmethod
    @api.marshal_with(genre_list)
    def get(id):
        """Find a genre by the ID."""
        return genre_service.get_a_genre(id)

    @staticmethod
    def delete(id):
        """Deletes a genre."""
        return genre_service.delete_genre(id)


@api.route('/<int:id>/books')
class GenreBookCollection(Resource):
    @api.marshal_with(genre_books_list)
    def get(self, id):
        """Find the genre books."""
        return genre_service.get_genre_books(id)
