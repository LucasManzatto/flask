import pytest
from backend.src.main import create_app, db
from backend.src.main.model.author import Author
from backend.src.main.model.books import Book
from backend.src.main.model.series import Series

from backend.src import blueprint


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
    for author in authors:
        author.series = []
    for serie in series:
        serie.books = []
    db.session.query(Series).delete()
    db.session.query(Book).delete()
    db.session.query(Author).delete()

    author = Author(id=1, name='Test')
    author_with_book = Author(id=2, name='Test With Book')
    author_with_series = Author(id=3, name='Test With Series')
    author_with_series_and_books = Author(id=4, name='Test With Series and Books')

    series = Series(id=1, title='Test 1', description='Test')
    series_with_author = Series(id=2, title='Test 2', description='Test')

    book = Book(title="Test Book", description='Teste', author_id=author_with_book.id)
    book2 = Book(title="Test Book 2", description='Teste')

    db.session.bulk_save_objects([series, author_with_book, author, book])
    db.session.commit()

    author_with_series_and_books.series.append(series_with_author)
    author_with_series_and_books.books.append(book2)
    db.session.add(author_with_series_and_books)

    author_with_series.series.append(series_with_author)
    db.session.add(author_with_series)

    db.session.commit()
    yield db


@pytest.fixture(scope='session')
def _db():
    return db
