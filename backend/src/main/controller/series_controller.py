from flask import request
from flask_restplus import Resource

from backend.src.main.service.series_service import SeriesService
from backend.src.main.util.dto import SeriesDTO, base_args
from webargs import fields
from webargs.flaskparser import use_args

api = SeriesDTO.api

series_args = {
    "id": fields.Str(missing=''),
    "title": fields.Str(missing=''),
    "description": fields.Str(missing=''),
}
series_args.update(base_args)

series_service = SeriesService()


@api.route('/')
@api.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Series not found.', 500: 'Mapping Key Error'})
class SeriesCollection(Resource):
    @api.marshal_list_with(SeriesDTO.series_query, code=201)
    @use_args(series_args)
    def get(self, args):
        """List all series."""
        return series_service.get_all(args)

    @api.response(201, 'Series successfully created.')
    @api.expect(SeriesDTO.series_create)
    def post(self):
        """Creates a new series."""
        return series_service.upsert(request.json, update=False)

    @api.response(201, 'Series successfully updated.')
    @api.expect(SeriesDTO.series_update)
    def put(self):
        """Updates a series."""
        return series_service.upsert(request.json, update=True)


@api.route('/<int:id>')
class SeriesItem(Resource):
    @api.marshal_with(SeriesDTO.series_list)
    def get(self, id):
        """Find a series by the ID."""
        return series_service.get_one(id)

    @api.response(200, 'Series successfully deleted.')
    def delete(self, id):
        """Deletes a series."""
        return series_service.delete(id, {'key': 'books'})


@api.route('/<int:id>/books')
class SeriesBookCollection(Resource):
    @api.marshal_with(SeriesDTO.series_books)
    def get(self, id):
        """Find the series books."""
        return series_service.get_model_fk(id, fk='books')


@api.route('/<int:id>/authors')
class SeriesAuthorCollection(Resource):
    @api.marshal_with(SeriesDTO.series_authors)
    def get(self, id):
        """Find the series authors."""
        return series_service.get_model_fk(id, fk='authors')
