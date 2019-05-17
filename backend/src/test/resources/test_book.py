# from main.model.author import Author
# from main.model.books import Book, BookSchema
#
# from main.util.utils import not_found, bad_request, message, conflict, \
#     success, created
#
#
# def test_get_one_book(test_client, db_session):
#     db_book = db_session.query(Book).first()
#     response = test_client.get(f"/books/{db_book.id}")
#     book = response.json
#     assert success(response)
#     assert book['title'] == db_book.title
#
#
# def test_get_all_books(test_client, db_session):
#     db_books_size = db_session.query(Book).count()
#     response = test_client.get("/books/")
#     books_size = len(response.json['books'])
#     assert success(response)
#     assert db_books_size == books_size
#
#
# def test_get_book_author(db_session, test_client):
#     book = db_session.query(Book).first()
#     response = test_client.get(f'/books/author/{book.id}')
#     author = response.json
#     assert success(response)
#     assert author['name'] == book.author.name
#
#
# def test_get_book_not_found(test_client):
#     response = test_client.get("/books/-1")
#     assert not_found(response)
#
#
# def test_insert_book(test_client, db_session):
#     book_json = {'title': 'Test Book New',
#                  'description': 'Teste',
#                  'author_id': 1,
#                  }
#     response = test_client.post('/books/', json=book_json)
#     assert created(response)
#     assert message(response, "Book successfully created.")
#     book = db_session.query(Book).filter_by(title='Test Book New').first()
#     assert book
#
#
# def test_insert_book_missing_arguments(test_client, db_session):
#     book_json = {
#         'description': 'Teste'
#     }
#     response = test_client.post('/books/', json=book_json)
#     assert bad_request(response)
#     book = db_session.query(Book).filter_by(title='Test Book New').first()
#     assert not book
#
#
# def test_insert_book_duplicated(test_client, db_session):
#     book = db_session.query(Book).first()
#     book_json = BookSchema().dump(book)
#     response = test_client.post('/books/', json=book_json)
#     assert conflict(response)
#     assert db_session.query(Book).filter_by(title=book.title).count() == 1
#
#
# def test_update_book(db_session, test_client):
#     book_json = {
#         'id': 1,
#         'title': 'Test Update',
#         'description': 'Test',
#         'author_id': 1}
#     response = test_client.put('/books/', json=book_json)
#     book = db_session.query(Book).get(book_json['id'])
#     assert success(response)
#     assert book.title == 'Test Update'
#
#
# def test_delete_book(db_session, test_client):
#     id = 1
#     response = test_client.delete(f'/books/{id}')
#     book = db_session.query(Book).get(id)
#     assert success(response)
#     assert not book
#
#
# def test_delete_book_not_found(db_session, test_client):
#     old_total = db_session.query(Book).count()
#     response = test_client.delete(f'/books/-1')
#     total = db_session.query(Book).count()
#     assert not_found(response)
#     assert total == old_total
