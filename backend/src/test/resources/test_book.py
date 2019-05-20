from backend.src.main.model.books import Book, BookSchema

from backend.src.main.util.utils import not_found, success
from backend.src.test.resources.generics import GenericTests

endpoint = 'books'
model = Book
model_schema = BookSchema()
filter_by = Book.title
filter_by_key = 'title'

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
                             filter_by_key=filter_by_key)


def test_get_one_book(test_client, db_session):
    generic_tests.get_one(test_client=test_client, db_session=db_session)


def test_get_all_books(test_client, db_session):
    generic_tests.get_all(test_client=test_client, db_session=db_session)


def test_get_book_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_insert_book(test_client, db_session):
    book = Book(title='Test Insert', description='Teste', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, data=book)


def test_insert_book_with_id(test_client, db_session):
    book = Book(id=1, title='Test Insert', description='Teste', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, data=book)


def test_insert_book_with_genres(test_client, db_session):
    book_json = {
        'title': 'Test Insert',
        'description': 'test',
        'author_id': 1,
        'genre_ids': [1]
    }
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data=book_json)


def test_insert_book_duplicated(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, existing=True)


def test_insert_book_missing_arguments(test_client, db_session):
    generic_tests.insert(db_session=db_session, test_client=test_client, json_data={}, missing_arguments=True)


def test_update_book(db_session, test_client):
    book = Book(id=1, title='Test Update', description='Test', author_id=1)
    generic_tests.insert(db_session=db_session, test_client=test_client, update=True, data=book)


def test_delete_book(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=1)


def test_delete_book_not_found(db_session, test_client):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=-1, found=False)


def test_get_book_author(db_session, test_client):
    book = db_session.query(Book).first()
    response = test_client.get(f'/books/author/{book.id}')
    author = response.json
    assert success(response)
    assert author['name'] == book.author.name
