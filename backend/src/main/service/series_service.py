from backend.src.main import db
from flask_restplus import abort
from main.model.books import Book
from main.model.series import Series, SeriesSchema


def create_series(data):
    series = Series.query.filter_by(title=data['title']).first()
    if not series:
        books_ids = data.pop('books_ids', [])
        new_series = SeriesSchema().load(data).data
        if new_series:
            db.session.add(new_series)
            db.session.flush()
            if books_ids:
                Book.query.filter(Book.id.in_(books_ids)).update({Book.series_id: new_series.id},
                                                                 synchronize_session='fetch')
            response_object = {
                'status': 'success',
                'message': 'Series successfully registered.'
            }
            db.session.commit()
            return response_object, 201
        else:
            abort(400, "No author with such ID.")
    else:
        response_object = {
            'status': 'fail',
            'message': 'Series already exists. Please choose another title.',
        }
        return response_object, 409


def update_series(series):
    books_ids = series.pop('books_ids', [])
    series_id = series['id']
    if books_ids:
        Book.query.filter(Book.series_id == series_id).update({Book.series_id: None},
                                                              synchronize_session='fetch')
        Book.query.filter(Book.id.in_(books_ids)).update({Book.series_id: series_id},
                                                         synchronize_session='fetch')
    Series.query.filter_by(id=series['id']).update(series)
    db.session.commit()
    return None, 201


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
