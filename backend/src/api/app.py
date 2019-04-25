from flask import jsonify, request
from backend.src.entities.entity import Book, BookSchema, app, api, db
from flask_restplus import Resource, fields

ns = api.namespace('books', description='Operations related to books')

book = api.model('Book', {
    'id': fields.String(readOnly=True, description='The ID of the book.'),
    'title': fields.String(readOnly=True, description='The title of the book.'),
    'description': fields.String(required=True, description='The description of the book.')
})


@ns.route('/')
@ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'Book not found.', 500: 'Mapping Key Error'})
class BooksCollection(Resource):
    @ns.marshal_list_with(book, code=201)
    def get(self):
        """List all books."""
        return Book.query.all()

    @ns.response(201, 'Book successfully created.')
    @ns.expect(book)
    def post(self):
        """Creates a new book."""
        new_book = BookSchema().load(request.json).data
        db.session.add(new_book)
        db.session.commit()
        return None, 201

    @ns.response(201, 'Book successfully updated.')
    @ns.expect(book)
    def put(self):
        """Updates a book."""
        book_id = request.json['id']
        Book.query.filter_by(id=book_id).update(request.json)
        db.session.commit()
        return None, 201


@ns.route('/<int:id>')
class BookItem(Resource):
    @ns.marshal_with(book)
    def get(self, id):
        """Find a book by the ID."""
        return Book.query.get_or_404(id)

    @ns.response(201, 'Book successfully deleted.')
    def delete(self, id):
        """Deletes a
         book."""
        Book.query.filter_by(id=id).delete()
        db.session.commit()
        return None, 201


app.run(debug=True)
