from flask_restplus import abort
from flask_restplus._http import HTTPStatus
from backend.src.main.model.genre import Genre
from marshmallow import ValidationError

from backend.src.main import db
from backend.src.main.model.author import Author
from backend.src.main.model.books import Book, BookSchema
from backend.src.main.model.series import Series
from backend.src.main.util.utils import response_success, response_conflict, response_created, response_bad_request
from sqlalchemy import or_, and_


def upsert_book(data, update):
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
                return update_existing_book(data, genres) if update else create_new_book(new_book, genres)
            elif new_book.series_id:
                return response_bad_request("Series doesn't exist.")
        else:
            return response_bad_request("Author doesn't exist.")
    else:
        return response_conflict('Book already exists. Please choose another title.')


def get_genres(data):
    genre_ids = data.pop('genre_ids', [])
    return Genre.query.filter(Genre.id.in_(genre_ids)).all()


def update_existing_book(data, genres):
    book = Book.query.get(data['id'])
    book.genres = genres
    Book.query.filter_by(id=data['id']).update(data)
    db.session.commit()
    return response_success("Book successfully updated.")


def get_all_books(args):
    query_all = get_query(args["query_all"])
    query_by_column = get_query(args['id'], args['title'], args['author'])
    query_filter = Book.query.join(Author).filter(query_all, query_by_column).paginate(page=0, error_out=False,
                                                                                       max_per_page=10)
    return query_filter


def get_query(id, title=None, author_name=None):
    filter_all = False

    if not title and not author_name:
        title = id
        author_name = id
        filter_all = True

    id_query = Book.id.like(wildcard(id))
    title_query = Book.title.like(wildcard(title))
    author_query = Author.name.like(wildcard(author_name))

    return or_(id_query, title_query, author_query) if filter_all else and_(id_query, title_query, author_query)


def wildcard(column):
    return f'%{column}%'


def get_a_book(book_id):
    return Book.query.get_or_404(book_id)


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


def delete_book(book_id):
    Book.query.filter_by(id=book_id).delete(synchronize_session=False)
    db.session.commit()
    return response_success('Book successfully deleted.')


def create_new_book(data, genres):
    del data.id
    data.genres = genres
    db.session.add(data)
    db.session.commit()
    return response_created('Book successfully created.')
