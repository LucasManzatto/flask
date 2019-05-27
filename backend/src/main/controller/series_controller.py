from flask import request
from flask_restplus import Resource

from backend.src.main.service import series_service
from backend.src.main.util.dto import SeriesDTO
from webargs import fields
from webargs.flaskparser import use_args

api = SeriesDTO.api

series_args = {
    "query_all": fields.Str(missing=''),
    "id": fields.Str(missing=''),
    "title": fields.Str(missing=''),
    "description": fields.Str(missing=''),
}


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Series not found.', 500: 'Mapping Key Error'})
class SeriesCollection(Resource):
    @api.marshal_list_with(SeriesDTO.series_query, code=201)
    @use_args(series_args)
    def get(self, args):
        """List all series."""
        return series_service.get_all_series(args)

    @api.response(201, 'Series successfully created.')
    @api.expect(SeriesDTO.series_create)
    def post(self):
        """Creates a new series."""
        return series_service.upsert_series(request.json, update=False)

    @api.response(201, 'Series successfully updated.')
    @api.expect(SeriesDTO.series_update)
    def put(self):
        """Updates a series."""
        return series_service.upsert_series(request.json, update=True)


@api.route('/<int:id>')
class SeriesItem(Resource):
    @api.marshal_with(SeriesDTO.series_list)
    def get(self, id):
        """Find a series by the ID."""
        return series_service.get_a_series(id)

    @api.response(200, 'Series successfully deleted.')
    def delete(self, id):
        """Deletes a series."""
        return series_service.delete_series(id)


@api.route('/<int:id>/books')
class SeriesBookCollection(Resource):
    @api.marshal_with(SeriesDTO.series_books)
    def get(self, id):
        """Find the series books."""
        return series_service.get_series_books(id)


@api.route('/<int:id>/authors')
class SeriesAuthorCollection(Resource):
    @api.marshal_with(SeriesDTO.series_authors)
    def get(self, id):
        """Find the series authors."""
        return series_service.get_series_authors(id)
