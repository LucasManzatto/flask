import sqlalchemy
from backend.src.main import db
from main.model.author import Author, AuthorSchema
from main.model.series import Series
from main.util.utils import response_created, response_conflict, response_success, response_bad_request


def upsert_author(data, update):
    author_from_db = Author.query.filter_by(name=data['name']).first()
    if not author_from_db:
        series_ids = data.pop('series_ids', [])
        series = Series.query.filter(Series.id.in_(series_ids)).all()
        if update:
            author = Author.query.get(data['id'])
            author.series = series
            Author.query.filter(Author.id == data['id']).update(data)
            db.session.commit()
            return response_success('Author successfully updated.')
        else:

            author = AuthorSchema().load(data).data
            author.series = series
            save_changes(author)
            return response_created('Author successfully created.')
    else:
        return response_conflict('Author already exists. Please choose another name.')


def get_all_authors():
    return Author.query.all()


def get_an_author(author_id):
    return Author.query.get_or_404(author_id)


def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        if has_no_dependencies(author):
            Author.query.filter_by(id=author_id).delete()
            db.session.commit()
            return response_success('')
        else:
            return response_conflict("Author has dependencies and can't be deleted.")
    else:
        return response_bad_request("Author not found.")


def has_no_dependencies(author):
    return not author.books and not author.series


def save_changes(data):
    db.session.add(data)
    db.session.commit()
