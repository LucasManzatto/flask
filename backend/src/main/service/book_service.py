from backend.src.main import db
from flask_restplus import abort
from main.model.author import Author
from main.model.books import Book, BookSchema
from main.model.series import Series
from main.util.utils import response_success, response_conflict, response_created, response_bad_request


def upsert_book(data, update):
    book = Book.query.filter_by(title=data['title']).first()
    new_book = BookSchema().load(data).data
    if book and not update:
        return response_conflict('Book already exists. Please choose another title.')
    else:
        author = Author.query.filter(Author.id == new_book.author_id).first()
        series = Series.query.filter(Series.id == new_book.series_id).first()
        if author:
            if series or not new_book.series_id:
                return update_existing_book(data) if update else create_new_book(new_book)
            elif new_book.series_id:
                return response_bad_request("Series doesn't exist.")
        else:
            if not new_book.author_id:
                return response_bad_request("Author field is required.")
            return response_bad_request("Author doesn't exist.")


def update_existing_book(data):
    Book.query.filter_by(id=data['id']).update(data)
    db.session.commit()
    return response_success("Book successfully updated.")


def get_all_books():
    return Book.query.all()


def get_a_book(book_id):
    return Book.query.get_or_404(book_id)


def get_book_author(book_id):
    book = Book.query.get(book_id)
    if book:
        return book.author if book.author_id else abort(400, 'Book has no author.')
    else:
        abort(400, 'Book not found.')


def delete_book(book_id):
    Book.query.filter_by(id=book_id).delete(synchronize_session=False)
    db.session.commit()
    return response_success('Book successfully deleted.')


def create_new_book(data):
    db.session.add(data)
    db.session.commit()
    return response_created('Book successfully created.')
