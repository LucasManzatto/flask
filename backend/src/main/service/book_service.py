from backend.src.main import db
from backend.src.main.model.books import Book, BookSchema


def save_new_user(data):
    book = Book.query.filter_by(title=data['title']).first()
    if not book:
        new_book = BookSchema().load(data).data
        save_changes(new_book)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def update_book(book):
    Book.query.get(book['id']).update(book)
    db.session.commit()
    return None, 201


def get_all_users():
    return Book.query.all()


def get_a_book(id):
    return Book.query.get_or_404(id)


def delete_book(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
