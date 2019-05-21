import pytest
from backend.src.main import create_app, db
from backend.src.main.model.series import Series
import backend.src.main.model.books as book_model
import backend.src.main.model.author as author_model
from backend.src.main.model.author import Author

from backend.src import blueprint
from main.model.genre import Genre


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('test')
    flask_app.register_blueprint(blueprint)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='function', autouse=True)
def init_database(test_client):
    # for table in reversed(db.metadata.sorted_tables):
    #     db.session.execute(table.delete())
    authors = db.session.query(Author).all()
    series = db.session.query(Series).all()
    genres = db.session.query(Genre).all()
    for author in authors:
        author.series = []
    for serie in series:
        serie.books = []
    for genre in genres:
        genre.books = []
    db.session.query(Series).delete()
    db.session.query(book_model.Book).delete()
    db.session.query(Author).delete()
    db.session.query(Genre).delete()

    book_model.BookFactory()
    book_model.BookWithAuthorFactory()
    author_model.AuthorFactory()
    author_model.AuthorFactory(books=3)

    # author_with_book = Author(id=2, name='Test With Book')
    # author_with_series = Author(id=3, name='Test With Series')
    # author_with_series_and_books = Author(id=4, name='Test With Series and Books')
    # author5 = Author(id=5, name='Test')
    #
    # series = Series(id=1, title='Test 1', description='Test')
    # series_with_author = Series(id=2, title='Test 2', description='Test')
    # series_with_books = Series(id=3, title='Test 3', description='Test')
    #
    # book = Book(title="Test", description='Teste')
    # book2 = Book(title="Test 2", description='Teste')
    # book_with_genre = Book(title="Test 3", description='Teste')
    # book4 = Book(title="Test 4", description='Teste', author_id=author5.id)
    #
    # genre = Genre(name='Test 5')
    #
    # db.session.bulk_save_objects([series, author5])
    # db.session.commit()
    #
    # series_with_books.books.append(book4)
    # db.session.add(series_with_books)
    #
    # author_with_book.books.append(book)
    # db.session.add(author_with_book)
    #
    # book_with_genre.genres.append(genre)
    # db.session.add(book_with_genre)
    #
    # author_with_series_and_books.series.append(series_with_author)
    # author_with_series_and_books.books.append(book2)
    # db.session.add(author_with_series_and_books)
    #
    # author_with_series.series.append(series_with_author)
    # db.session.add(author_with_series)

    db.session.commit()
    yield db


@pytest.fixture(scope='session')
def _db():
    return db
