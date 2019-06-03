from flask_restplus._http import HTTPStatus
from backend.src.main.service import utils
from marshmallow import ValidationError

from backend.src.main import db
from backend.src.main.model.books import Book
from backend.src.main.model.series import Series, SeriesSchema
from backend.src.main.util.utils import response_created, response_success, response_conflict, response_bad_request
from sqlalchemy import or_, and_


def upsert_series(data, update):
    books = get_books(data)

    try:
        new_series = SeriesSchema().load(data)
    except ValidationError as err:
        return response_bad_request(err.messages)

    series = Series.query.filter_by(title=data['title']).first()
    if not series or update:
        return update_series(books, data) if update else create_series(books, new_series)
    else:
        return response_conflict('Series already exists. Please choose another title.')


def get_books(data):
    books_ids = data.pop('books_ids', [])
    books = Book.query.filter(Book.id.in_(books_ids)).all()
    return books


def create_series(books, new_series):
    del new_series.id
    new_series.books = books
    db.session.add(new_series)
    db.session.commit()
    return response_created('Series created successfully.')


def update_series(books, data):
    new_series = Series.query.get(data['id'])
    new_series.books = books
    Series.query.filter_by(id=data['id']).update(data)
    db.session.commit()
    return response_success('Series updated successfully.')


def get_all_series(args):
    page = args.pop('page', 0)
    page_size = int(args.pop('per_page', 10))
    sort_query = utils.get_sort_query(args, Series)
    sub_queries = utils.get_query(Series, args)
    query_filter = Series.query.filter(*sub_queries).order_by(sort_query).paginate(page=page, error_out=False,
                                                                                   max_per_page=page_size)
    return query_filter


def get_a_series(series_id):
    return Series.query.get_or_404(series_id)


def get_series_books(series_id):
    books = Series.query.get(series_id).books
    return books


def get_series_authors(series_id):
    authors = Series.query.get(series_id).authors
    return authors


def delete_series(series_id):
    Book.query.filter(Book.series_id == series_id).update({Book.series_id: None},
                                                          synchronize_session='fetch')
    Series.query.filter_by(id=series_id).delete()
    db.session.commit()
    return response_success('')


def save_changes(data):
    db.session.add(data)
    db.session.commit()
