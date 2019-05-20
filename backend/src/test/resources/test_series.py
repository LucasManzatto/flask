# from main.model.books import Book
# from main.model.series import Series, SeriesSchema
# from main.util.utils import not_found, bad_request, message, conflict, \
#     success, created


# def test_get_all_series(test_client, db_session):
#     db_series_size = db_session.query(Series).count()
#     response = test_client.get('/series/')
#     series_size = len(response.json['series'])
#     assert success(response)
#     assert db_series_size == series_size
#
#
# def test_get_a_series(test_client, db_session):
#     db_series = db_session.query(Series).first()
#     response = test_client.get(f'/series/{db_series.id}')
#     series = response.json
#     assert success(response)
#     assert db_series.id == series['id']
#
#
# def test_create_series(test_client, db_session):
#     series_json = {
#         'title': 'Test Insert',
#         'description': 'Test',
#     }
#     response = test_client.post('/series/', json=series_json)
#     series = db_session.query(Series).filter_by(title=series_json['title']).first()
#     assert created(response)
#     assert message(response, 'Series created successfully.')
#     assert series
#
#
# def test_create_series_missing_arguments(test_client, db_session):
#     series_json = {
#         'description': 'Test',
#     }
#     response = test_client.post('/series/', json=series_json)
#     assert bad_request(response)
#
#
# def test_create_duplicated_series(test_client, db_session):
#     series = db_session.query(Series).first()
#     series_json = SeriesSchema().dump(series)
#
#     response = test_client.post('/series/', json=series_json)
#     series_size = db_session.query(Series).filter_by(title=series.title).count()
#     assert conflict(response)
#     assert series_size == 1
#
#
# def test_create_series_with_books(test_client, db_session):
#     series_json = {
#         'title': 'Test Insert',
#         'books_ids': [1]
#     }
#     response = test_client.post('/series/', json=series_json)
#     series = db_session.query(Series).filter_by(title=series_json['title']).first()
#     assert created(response)
#     assert series
#     assert len(series.books) == len(series_json['books_ids'])
#
#
# def test_create_series_with_invalid_books(test_client, db_session):
#     series_json = {
#         'title': 'Test Insert 3',
#         'description': 'Test',
#         'books_ids': [-1]
#     }
#     response = test_client.post('/series/', json=series_json)
#     series = db_session.query(Series).filter_by(title='Test Insert 3').first()
#     assert created(response)
#     assert series
#     assert not series.books
#
#
# def test_update_series(test_client, db_session):
#     series_json = {
#         'id': 1,
#         'title': 'Test Update',
#         'books_ids': [1]
#     }
#     response = test_client.put('/series/', json=series_json)
#     series = db_session.query(Series).filter_by(id=series_json['id']).first()
#     assert success(response)
#     assert series.title == series_json['title']
