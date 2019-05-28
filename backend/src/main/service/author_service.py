from backend.src.main.service import utils
from marshmallow import ValidationError, INCLUDE

from backend.src.main import db
from backend.src.main.model.author import Author, AuthorSchema
from backend.src.main.model.series import Series
from backend.src.main.util.utils import response_created, response_conflict, response_success, response_bad_request
from sqlalchemy import or_, and_


def upsert_author(data, update):
    series = get_series(data)
    try:
        author = AuthorSchema(unknown=INCLUDE).load(data)
    except ValidationError as err:
        print(err.messages)
        return response_bad_request(err.messages)

    author_from_db = Author.query.filter_by(name=data['name']).first()
    if not author_from_db:
        return update_existing_author(data, series) if update \
            else create_new_author(author, series)
    else:
        return response_conflict('Author already exists. Please choose another name.')


def get_series(data):
    series_ids = data.pop('series_ids', [])
    series = Series.query.filter(Series.id.in_(series_ids)).all()
    return series


def create_new_author(new_author, series):
    del new_author.id
    new_author.series = series
    save_changes(new_author)
    return response_created('Author successfully created.')


def update_existing_author(data, series):
    author = Author.query.get(data['id'])
    author.series = series
    Author.query.filter(Author.id == data['id']).update(data)
    db.session.commit()
    return response_success('Author successfully updated.')


def get_all_authors(args):
    page = args.pop('page', 0)
    sort_query = utils.get_sort_query(args, Author)
    sub_queries = utils.get_query(Author, args)
    query = Author.query.filter(*sub_queries).order_by(sort_query).paginate(page=page, error_out=False, max_per_page=10)
    return query


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


def get_author_books(id):
    books = Author.query.get(id).books
    return books


def get_author_series(id):
    return Author.query.get(id).series


def has_no_dependencies(author):
    return not author.books and not author.series


def save_changes(data):
    db.session.add(data)
    db.session.commit()
