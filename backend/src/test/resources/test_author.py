from main.util.utils import message, success, created, conflict
from main.model.author import Author, AuthorSchema
from test.resources.generics import GenericTests

endpoint = 'authors'
model = Author
model_schema = AuthorSchema()
filter_by = Author.name
filter_by_key = 'name'

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
                             filter_by_key=filter_by_key)


def test_get_one_author(test_client, db_session):
    generic_tests.get_one(test_client, db_session)


def test_get_all_authors(test_client, db_session):
    generic_tests.get_all(test_client, db_session)


def test_get_author_not_found(test_client):
    generic_tests.get_not_found(test_client)


def test_insert_author(test_client, db_session):
    author = Author(name='Test Insert')
    generic_tests.insert(db_session, test_client, data=author)


def test_insert_existing_author(test_client, db_session):
    generic_tests.insert(db_session, test_client, existing=True)


def test_insert_author_with_series(test_client, db_session):
    author_json = {
        'name': 'Test Create',
        'series_ids': [1]
    }
    generic_tests.insert(db_session, test_client, json_data=author_json)


def test_update_author(test_client, db_session):
    author_json = {
        'id': 1,
        'name': 'Test Update',
        'series_ids': [1]
    }
    generic_tests.insert(db_session, test_client, json_data=author_json, update=True)


def test_delete_author(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=1)


def test_delete_author_with_books(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=2, has_fk=True)


def test_delete_author_with_series(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=3, has_fk=True)


def test_delete_author_with_series_and_books(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=4, has_fk=True)
