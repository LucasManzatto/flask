from main.util.utils import not_found, response_success, bad_request, response_created, message, response_conflict, \
    success, created, conflict
from main.model.author import Author


def test_get_all_authors(init_database, test_client, db_session):
    authors_from_db_size = db_session.query(Author).count()
    response = test_client.get('/authors/')
    authors_size = len(response.json['authors'])
    assert success(response)
    assert authors_from_db_size == authors_size


def test_get_author(init_database, test_client, db_session):
    author_from_db = db_session.query(Author).first()
    response = test_client.get(f'/authors/{author_from_db.id}')
    author = response.json
    assert success(response)
    assert author['id'] == author_from_db.id


def test_create_author(init_database, test_client, db_session):
    author_json = {
        'name': 'Test Create'
    }
    response = test_client.post('/authors/', json=author_json)
    assert created(response)
    assert message(response, "Author successfully created.")
    assert db_session.query(Author).filter_by(name='Test Create').first()


def test_create_existing_author(init_database, test_client, db_session):
    author_json = {
        'name': 'Test Create'
    }
    response = test_client.post('/authors/', json=author_json)
    assert conflict(response)
    assert db_session.query(Author).filter_by(name='Test Create').count() == 1


def test_create_author_with_series(init_database, test_client, db_session):
    author_json = {
        'name': 'Test Create 2',
        'series_ids': [1]
    }
    response = test_client.post('/authors/', json=author_json)
    author = db_session.query(Author).filter_by(name='Test Create 2').first()
    assert created(response)
    assert message(response, "Author successfully created.")
    assert author
    assert author.series[0].id == author_json['series_ids'][0]


def test_update_author(init_database, test_client, db_session):
    author_json = {
        'id': 1,
        'name': 'Test Update'
    }
    response = test_client.put('/authors/', json=author_json)
    author = db_session.query(Author).get(1)
    assert success(response)
    assert message(response, "Author successfully updated.")
    assert author_json['name'] == author.name
