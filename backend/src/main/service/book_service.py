from backend.src.main import db
from flask_restplus import abort
from main.model.author import Author
from main.model.books import Book, BookSchema


def create_book(data):
    book = Book.query.filter_by(title=data['title']).first()
    if not book:
        new_book = BookSchema().load(data).data
        author = Author.query.get(new_book.author_id)
        if author:
            save_changes(new_book)
            response_object = {
                'status': 'success',
                'message': 'Book successfully registered.'
            }
            return response_object, 201
        else:
            abort(400, "No author with such ID.")
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book already exists. Please choose another title.',
        }
        return response_object, 409


def update_book(book):
    Book.query.filter_by(id=book['id']).update(book)
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
            abort(400, 'Book has no author.')
    else:
        abort(400, 'Book not found.')


def delete_book(book_id):
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
