import pytest
from backend.src.main import create_app, db
from backend.src.main.model.series import Series
from backend.src.main.model.author import Author, AuthorFactory

from backend.src import blueprint
from backend.src.main.model.books import Book, BookFactory
from main.model.genre import Genre, GenreFactory


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
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())

    BookFactory()
    AuthorFactory()
    AuthorFactory(books=1)
    GenreFactory()
    GenreFactory(books=1)

    db.session.commit()
    yield db


@pytest.fixture(scope='session')
def _db():
    return db
