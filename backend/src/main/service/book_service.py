from backend.src.main import db
from backend.src.main.model.books import Book, BookSchema
from flask_restplus import abort


def create_book(data):
    book = Book.query.filter_by(title=data['title']).first()
    if not book:
        new_book = BookSchema().load(data).data
        save_changes(new_book)
        response_object = {
            'status': 'success',
            'message': 'Book successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book already exists. Please choose another title.',
        }
        return response_object, 409


def update_book(book):
    Book.query.get(book['id']).update(book)
    db.session.commit()
    return None, 201


def get_all_books():
    return Book.query.all()


def get_a_book(book_id):
    return Book.query.get_or_404(book_id)


def get_book_author(book_id):
    book = Book.query.get(book_id)
    if book:
        if book.author_id:
            return book.author
        else:
            abort(404, 'Book has no author.')
    else:
        abort(404, 'Book not found.')


def delete_book(book_id):
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
