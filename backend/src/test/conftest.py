import os

import pytest
from flask_sqlalchemy import SQLAlchemy
from main import create_app, db
from main.model.author import Author
from main.model.books import Book
from src import blueprint


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('test')
    flask_app.register_blueprint(blueprint)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='session')
def init_database(test_client):
    print('test')
    # Create the database and the database table
    # db.drop_all()
    # db.create_all()
    db.session.query(Book).delete()
    db.session.query(Author).delete()
    db.session.commit()

    author = Author(name='Test')
    book1 = Book(title="Test Book", description='Teste', author_id=1)
    book2 = Book(title="Test Book 2", description='Teste', author_id=1)
    db.session.add(author)
    db.session.commit()

    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()

    yield db  # this is where the testing happens!


@pytest.yield_fixture(scope='function')
def session(init_database):
    db.session.begin_nested()
    yield db.session
    db.session.rollback()


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    app.register_blueprint(blueprint)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


# @pytest.fixture(scope='session')
# def testapp(app):
#     return app.test_client()
#
#
@pytest.fixture(scope='session')
def _db():
    return db

# @pytest.fixture(scope='function', autouse=True)
# def session(_db):
#     connection = _db.engine.connect()
#     transaction = connection.begin()
#
#     options = dict(bind=connection, binds={})
#     session_ = _db.create_scoped_session(options=options)
#
#     _db.session = session_
#
#     yield session_
#
#     transaction.rollback()
#     connection.close()
#     session_.remove()
