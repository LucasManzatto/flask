from backend.src.main import db
from flask_restplus import abort
from main.model.books import Book, BookSchema
from main.model.series import Series, SeriesSchema
from main.util.utils import response_created, response_success, response_conflict


def upsert_series(data, update):
    series = Series.query.filter_by(title=data['title']).first()
    if not series or update:
        books_ids = data.pop('books_ids', [])
        books = Book.query.filter(Book.id.in_(books_ids)).all()
        if update:
            new_series = Series.query.get(data['id'])
            new_series.books = books
            Series.query.filter_by(id=data['id']).update(data)
            db.session.commit()
            return response_success('Series updated successfully.')
        else:
            new_series = SeriesSchema().load(data).data
            new_series.books = books
            db.session.commit()
            return response_created('Series created successfully.')
    else:
        return response_conflict('Series already exists. Please choose another title.')


def get_all_series():
    return Series.query.all()


def get_a_series(series_id):
    return Series.query.get_or_404(series_id)


def delete_series(series_id):
    Book.query.filter(Book.series_id == series_id).update({Book.series_id: None},
                                                          synchronize_session='fetch')
    Series.query.filter_by(id=series_id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
