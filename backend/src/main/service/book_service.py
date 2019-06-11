from flask_restplus import abort
from flask_restplus._http import HTTPStatus
from backend.src.main.model.genre import Genre
from backend.src.main.service import utils
from marshmallow import ValidationError

from backend.src.main import db
from backend.src.main.model.author import Author
from backend.src.main.model.books import Book, BookSchema
from backend.src.main.model.series import Series
from backend.src.main.util.utils import response_success, response_conflict, response_created, response_bad_request
from sqlalchemy import or_, and_, text
from sqlalchemy.orm import joinedload


def upsert(data, update):
    genres = get_genres(data)
    try:
        new_book = BookSchema().load(data)
        del new_book.author
    except ValidationError as err:
        print(err.messages)
        return response_bad_request(err.messages)

    book = Book.query.filter_by(title=data['title']).first()
    if not book or update:
        author = Author.query.filter(Author.id == new_book.author_id).first()
        series = Series.query.filter(Series.id == new_book.series_id).first()
        if author:
            if series or not new_book.series_id:
                return update_item(data, genres) if update else create(new_book,
                                                                            {'key': 'genres', 'value': genres})
            elif new_book.series_id:
                return response_bad_request("Series doesn't exist.")
        else:
            return response_bad_request("Author doesn't exist.")
    else:
        return response_conflict('Book already exists. Please choose another title.')


def delete(book_id):
    Book.query.filter_by(id=book_id).delete(synchronize_session=False)
    db.session.commit()
    return response_success('Book successfully deleted.')


def create(data, *args):
    del data.id
    for arg in args:
        setattr(data, arg['key'], arg['value'])
    db.session.add(data)
    db.session.commit()
    return response_created('Book successfully created.')


def get_all(args):
    page = int(args.pop('page', 0))
    page_size = int(args.pop('per_page', 10))
    sort_query = utils.get_sort_query(args, Book)
    sub_queries = utils.get_query(Book, args)
    query_filter = Book.query.join(Author).options(joinedload('author')).filter(*sub_queries).order_by(
        sort_query).paginate(page=page,
                             error_out=False,
                             max_per_page=page_size)
    return query_filter


def get_one(book_id):
    return Book.query.get_or_404(book_id)


def get_genres(data):
    genre_ids = data.pop('genre_ids', [])
    return Genre.query.filter(Genre.id.in_(genre_ids)).all()


def update_item(data, genres):
    book = Book.query.get(data['id'])
    book.genres = genres
    Book.query.filter_by(id=data['id']).update(data)
    db.session.commit()
    return response_success("Book successfully updated.")


def get_book_author(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(HTTPStatus.NOT_FOUND, 'Book not found.')
    return book.author


def get_book_genres(book_id):
    return Genre.query.join(Genre.books).filter(Book.id == book_id).all()


def get_book_series(book_id):
    series = Book.query.get(book_id).series
    return series
