from flask import jsonify, request
from backend.src.entities.entity import Book, BookSchema, app, api, db
from flask_restplus import Resource, fields

ns = api.namespace('books', description='Operations related to books')

book = api.model('Book', {
    'title': fields.String(readOnly=True, description='The title of the book.'),
    'description': fields.String(required=True, description='The description of the book.')
})


# teste
@ns.route('/')
class BooksCollection(Resource):
    @ns.marshal_list_with(book, code=201)
    def get(self):
        """List all books."""
        return Book.query.all()

    @api.response(201, 'Category successfully created.')
    @ns.expect(book)
    @ns.marshal_with(book, code=201)
    def post(self):
        """Creates a new blog category."""
        new_book = BookSchema().load(request.json).data
        db.session.add(new_book)
        db.session.commit()
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Book not found.')
class BookItem(Resource):
    @api.param('id', "The Book's ID")
    @ns.marshal_with(book, code=201)
    def get(self, id):
        return Book.query.get_or_404(id)


if __name__ == "__app__":
    app.run(debug=True)
