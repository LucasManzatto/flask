from main.model.books import Book

from main.util.utils import not_found, bad_request, message, conflict, \
    success, created


def book_test():
    return Book(title="Test Book", description='Teste', author_id=1)


def test_insert_book(test_client, init_database, session):
    response = test_client.post('/books/', json={'title': 'Test Book New', 'description': 'Teste', 'author_id': '1'
                                                 })
    assert created(response)
    assert message(response, "Book successfully created.")
    assert session.query(Book).filter_by(title='Test Book New').first()


def test_insert_existing_book(test_client, init_database, session):
    response = test_client.post('/books/', json={'title': 'Test Book New', 'description': 'Teste', 'author_id': '1'
                                                 })
    assert conflict(response)
    assert session.query(Book).filter_by(title='Test Book New').count() == 1


def test_insert_book_without_author(test_client, init_database, db_session):
    book_json = {
        'title': 'Test',
        'description': 'Teste'}
    response = test_client.post('/books/', json=book_json)
    book = db_session.query(Book).filter_by(title='Test').first()
    assert not book
    assert bad_request(response)
    assert message(response, 'Author field is required.')


def test_insert_book_with_non_existing_author_fk(test_client, init_database, db_session):
    book_json = {
        'title': 'Test',
        'description': 'Test',
        'author_id': -1}
    response = test_client.post('/books/', json=book_json)
    book = db_session.query(Book).filter_by(title='Test').first()
    assert not book
    assert bad_request(response)
    assert message(response, "Author doesn't exist.")


def test_insert_book_with_non_existing_series_fk(test_client, init_database, db_session):
    book_json = {
        'title': 'Test',
        'description': 'Test',
        'author_id': 1,
        'series_id': -1}
    response = test_client.post('/books/', json=book_json)
    book = db_session.query(Book).filter_by(title='Test').first()
    assert bad_request(response)
    assert message(response, "Series doesn't exist.")
    assert not book


def test_get_book(init_database, test_client, db_session):
    db_book = db_session.query(Book).first()
    response = test_client.get(f"/books/{db_book.id}")
    book = response.json
    assert success(response)
    assert book['title'] == db_book.title


def test_get_all_books(init_database, test_client, db_session):
    db_books_size = db_session.query(Book).count()
    response = test_client.get("/books/")
    books_size = len(response.json['books'])
    assert success(response)
    assert db_books_size == books_size


def test_book_not_found(test_client, init_database):
    response = test_client.get("/books/-1")
    assert not_found(response)


def test_update_book(db_session, test_client, init_database):
    book_json = {
        'id': 1,
        'title': 'Test Update',
        'description': 'Test',
        'author_id': 1}
    response = test_client.put('/books/', json=book_json)
    book = db_session.query(Book).get(1)
    assert success(response)
    assert book.title == 'Test Update'


def test_get_book_author(db_session, test_client, init_database):
    book = db_session.query(Book).first()
    response = test_client.get(f'/books/author/{book.id}')
    author = response.json
    assert success(response)
    assert author['name'] == book.author.name


def test_delete_book_not_found(db_session, test_client, init_database):
    response = test_client.delete(f'/books/-1')
    total = db_session.query(Book).count()
    assert not_found(response)
    assert total == 3


def test_delete_book(db_session, test_client, init_database):
    response = test_client.delete(f'/books/1')
    book = db_session.query(Book).get(1)
    total = db_session.query(Book).count()
    assert success(response)
    assert not book
    assert total == 2
