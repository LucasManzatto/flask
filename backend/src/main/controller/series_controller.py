from flask import request
from flask_restplus import Resource
from main.service.series_service import get_all_series, create_series, update_series, get_a_series, delete_series
from ..util.dto import SeriesDTO

api = SeriesDTO.api
series_create = SeriesDTO.series_create
series_list = SeriesDTO.series_list


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Series not found.', 500: 'Mapping Key Error'})
class SeriesCollection(Resource):
    @api.marshal_list_with(series_list, code=201)
    def get(self):
        """List all series."""
        return get_all_series()

    @api.response(201, 'Series successfully created.')
    @api.expect(series_create)
    def post(self):
        """Creates a new series."""
        return create_series(request.json)

    @api.response(201, 'Series successfully updated.')
    @api.expect(series_create)
    def put(self):
        """Updates a series."""
        return update_series(request.json)


@api.route('/<int:id>')
class SeriesItem(Resource):
    @api.marshal_with(series_list)
    def get(self, id):
        """Find a series by the ID."""
        return get_a_series(id)

    @api.response(201, 'Series successfully deleted.')
    def delete(self, id):
        """Deletes a series."""
        return delete_series(id)
