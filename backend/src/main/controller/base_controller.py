# from flask import request
# from flask_restplus import Resource
#
# from backend.src.main.service import author_service
# from backend.src.main.util.dto import AuthorDTO, base_args
# from webargs import fields
# from webargs.flaskparser import use_args
#
# api = AuthorDTO.api
#
# author_args = {
#     "id": fields.Str(missing=''),
#     "name": fields.Str(missing='')
# }
# author_args.update(base_args)
#
#
# @api.route('/')
# @api.doc(
#     responses={200: 'OK', 201: 'Created', 400: 'Invalid Argument', 404: 'Author not found.', 500: 'Mapping Key Error'})
# class ClassCollection(Resource):
#     get_all = {}
#     create = {}
#     update = {}
#     service = {}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.get_all = args[0]
#         self.create = args[1]
#         self.update = args[2]
#         self.service = args[3]
#
#     @api.marshal_list_with(get_all, code=201)
#     @use_args(author_args)
#     def get(self, args):
#         """List all authors."""
#         return service.get_all_authors(args)
#
#     @api.expect(create)
#     def post(self):
#         """Creates a new author."""
#         return author_service.upsert_author(request.json, update=False)
#
#     @api.expect(update)
#     def put(self):
#         """Updates an author."""
#         return author_service.upsert_author(request.json, update=True)
#
#
# @api.route('/<int:id>')
# class BookItem(Resource):
#     @api.marshal_with(AuthorDTO.author_list)
#     def get(self, id):
#         """Find a author by the ID."""
#         return author_service.get_an_author(id)
#
#     @staticmethod
#     def delete(id):
#         """Deletes an author."""
#         return author_service.delete_author(id)
#
#
# @api.route('/<int:id>/books')
# class BookCollection(Resource):
#     @api.marshal_list_with(AuthorDTO.author_books)
#     def get(self, id):
#         """Find the author books."""
#         return author_service.get_author_books(id)
#
#
# @api.route('/<int:id>/series')
# class BookCollection(Resource):
#     @api.marshal_list_with(AuthorDTO.author_series)
#     def get(self, id):
#         """Find the author series."""
#         return author_service.get_author_series(id)