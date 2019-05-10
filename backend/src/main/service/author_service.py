from backend.src.main import db
from main.model.author import Author, AuthorSchema
from main.model.series import Series


def create_author(data):
    author = Author.query.filter_by(name=data['name']).first()
    if not author:
        series_ids = data.pop('series_ids', [])
        new_author = AuthorSchema().load(data).data

        series = Series.query.filter(Series.id.in_(series_ids)).all()
        new_author.series.extend(series)

        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Author successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Author already exists. Please choose another name.',
        }
        return response_object, 409


def update_author(author):
    series_ids = author.pop('series_ids', [])
    author_object = Author.query.get(author['id'])
    series = Series.query.filter(Series.id.in_(series_ids)).all()
    author_object.series = series
    Author.query.filter(Author.id == author['id']).update(author)
    db.session.commit()
    return None, 201


def get_all_authors():
    return Author.query.all()


def get_an_author(author_id):
    return Author.query.get_or_404(author_id)


def delete_author(author_id):
    Author.query.filter_by(id=author_id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
