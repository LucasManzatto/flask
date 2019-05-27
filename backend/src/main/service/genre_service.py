# from main.model.books import Book
from backend.src.main.model.genre import GenreSchema, Genre
from backend.src.main.model.books import Book
from marshmallow import ValidationError, INCLUDE

from backend.src.main import db
from backend.src.main.util.utils import response_created, response_conflict, response_success, response_bad_request


def upsert_genre(data, update):
    books = get_books(data)
    try:
        genre = GenreSchema(unknown=INCLUDE).load(data)
    except ValidationError as err:
        print(err.messages)
        return response_bad_request(err.messages)

    genre_from_db = Genre.query.filter_by(name=data['name']).first()
    if not genre_from_db:
        return update_existing_genre(data, books) if update \
            else create_new_genre(genre, books)
    else:
        return response_conflict('Genre already exists. Please choose another name.')


def get_books(data):
    books_ids = data.pop('books_ids', [])
    books = Book.query.filter(Book.id.in_(books_ids)).all()
    return books


def create_new_genre(new_genre, books):
    del new_genre.id
    new_genre.books = books
    save_changes(new_genre)
    return response_created('Genre successfully created.')


def update_existing_genre(data, books):
    genre = Genre.query.get(data['id'])
    genre.books = books
    Genre.query.filter(Genre.id == data['id']).update(data)
    db.session.commit()
    return response_success('Genre successfully updated.')


def get_all_genres():
    return Genre.query.all()


def get_a_genre(genre_id):
    return Genre.query.get_or_404(genre_id)


def delete_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if genre:
        genre.books = []
        Genre.query.filter_by(id=genre_id).delete()
        db.session.commit()
        return response_success('')
    else:
        return response_bad_request("Genre not found.")


def get_genre_books(genre_id):
    books = Genre.query.get(genre_id).books
    return books


def save_changes(data):
    db.session.add(data)
    db.session.commit()
