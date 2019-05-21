# from backend.src.main.model.author import Author, AuthorSchema
# from backend.src.test.resources.generics import GenericTests
# from sqlalchemy.orm import joinedload
#
# endpoint = 'authors'
# model = Author
# model_schema = AuthorSchema()
# filter_by = Author.name
# filter_by_key = 'name'
#
# generic_tests = GenericTests(endpoint=endpoint, model=model, model_schema=model_schema, filter_by=filter_by,
#                              filter_by_key=filter_by_key)
#
#
# def test_get_one_author(test_client, db_session):
#     generic_tests.get_one(test_client, db_session)
#
#
# def test_get_all_authors(test_client, db_session):
#     generic_tests.get_all(test_client, db_session)
#
#
# def test_get_author_books(test_client, db_session):
#     author = db_session.query(Author).join(Author.books).options(joinedload('books')).first()
#     generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='books',
#                                         object_from_db=author)
#
#
# def test_get_author_series(test_client, db_session):
#     author = db_session.query(Author).options(joinedload('series')).first()
#     generic_tests.get_relationship_data(test_client=test_client, db_session=db_session, relationship='series',
#                                         object_from_db=author)
#
#
# def test_get_author_not_found(test_client):
#     generic_tests.get_not_found(test_client)
#
#
# def test_insert_author(test_client, db_session):
#     author = Author(name='Test Insert')
#     generic_tests.insert(db_session, test_client, data=author)
#
#
# def test_insert_author_duplicated(test_client, db_session):
#     generic_tests.insert(db_session, test_client, existing=True)
#
#
# def test_author_missing_arguments(test_client, db_session):
#     generic_tests.insert(db_session, test_client, missing_arguments=True, json_data={})
#
#
# def test_insert_author_with_series(test_client, db_session):
#     author_json = {
#         'name': 'Test Create',
#         'series_ids': [1]
#     }
#     generic_tests.insert(db_session, test_client, json_data=author_json)
#
#
# def test_update_author(test_client, db_session):
#     author_json = {
#         'id': 1,
#         'name': 'Test Update',
#         'series_ids': [1]
#     }
#     generic_tests.insert(db_session, test_client, json_data=author_json, update=True)
#
#
# def test_delete_author(test_client, db_session):
#     generic_tests.delete(db_session=db_session, test_client=test_client, id=1)
#
#
# def test_delete_author_with_books(test_client, db_session):
#     generic_tests.delete(db_session=db_session, test_client=test_client, id=2, has_fk=True)
#
#
# def test_delete_author_with_series(test_client, db_session):
#     generic_tests.delete(db_session=db_session, test_client=test_client, id=3, has_fk=True)
#
#
# def test_delete_author_with_series_and_books(test_client, db_session):
#     generic_tests.delete(db_session=db_session, test_client=test_client, id=4, has_fk=True)
