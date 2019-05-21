from flask import request
from flask_restplus import Resource

from backend.src.main.service.series_service import get_all_series, upsert_series, get_a_series, delete_series, \
    get_series_books, get_series_authors
from ..util.dto import SeriesDTO

api = SeriesDTO.api
series_create = SeriesDTO.series_create
series_update = SeriesDTO.series_update
series_list = SeriesDTO.series_list


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Series not found.', 500: 'Mapping Key Error'})
class SeriesCollection(Resource):
    @api.marshal_list_with(series_list, code=201, envelope='series')
    def get(self):
        """List all series."""
        return get_all_series()

    @api.response(201, 'Series successfully created.')
    @api.expect(series_create)
    def post(self):
        """Creates a new series."""
        return upsert_series(request.json, update=False)

    @api.response(201, 'Series successfully updated.')
    @api.expect(series_update)
    def put(self):
        """Updates a series."""
        return upsert_series(request.json, update=True)


@api.route('/<int:id>')
class SeriesItem(Resource):
    @api.marshal_with(series_list)
    def get(self, id):
        """Find a series by the ID."""
        return get_a_series(id)

    @api.response(200, 'Series successfully deleted.')
    def delete(self, id):
        """Deletes a series."""
        return delete_series(id)


@api.route('/<int:id>/books')
class SeriesBookCollection(Resource):
    @api.marshal_with(SeriesDTO.series_books)
    def get(self, id):
        """Find the series books."""
        return get_series_books(id)


@api.route('/<int:id>/authors')
class SeriesAuthorCollection(Resource):
    @api.marshal_with(SeriesDTO.series_authors)
    def get(self, id):
        """Find the series authors."""
        return get_series_authors(id)
