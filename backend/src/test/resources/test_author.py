from main.util.utils import message, success, created, conflict
from main.model.author import Author, AuthorSchema
from test.resources.generics import GenericTests

endpoint = 'authors'
model = Author
model_schema = AuthorSchema()

generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema)


def test_get_one_author(test_client, db_session):
    generic_tests.get_one(test_client, db_session)


def test_get_all_authors(test_client, db_session):
    generic_tests.get_all(test_client, db_session)


def test_insert_author(test_client, db_session):
    author = Author(name='Test Create')
    generic_tests.insert(db_session, test_client, data=author)


def test_insert_existing_author(test_client, db_session):
    author = db_session.query(Author).first()
    generic_tests.insert(db_session, test_client, data=author, existing=True)


def test_insert_author_with_series(test_client, db_session):
    author_json = {
        'name': 'Test Create 2',
        'series_ids': [1]
    }
    response = test_client.post('/authors/', json=author_json)
    author = db_session.query(Author).filter_by(name=author_json['name']).first()
    assert created(response)
    assert message(response, "Author successfully created.")
    assert author
    assert author.series[0].id == author_json['series_ids'][0]


def test_update_author(test_client, db_session):
    author_json = {
        'id': 1,
        'name': 'Test Update',
        'series_ids': [1]
    }
    response = test_client.put('/authors/', json=author_json)
    author = db_session.query(Author).filter_by(name=author_json['name']).first()
    assert success(response)
    assert message(response, "Author successfully updated.")
    assert author_json['name'] == author.name
    assert author.series[0].id == author_json['series_ids'][0]


def test_delete_author(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=1)


def test_delete_author_with_books(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=2, has_fk=True)


def test_delete_author_with_series(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=3, has_fk=True)


def test_delete_author_with_series_and_books(test_client, db_session):
    generic_tests.delete(db_session=db_session, test_client=test_client, id=4, has_fk=True)
