from backend.src.main.model.books import Book

book1 = Book("Test 4", "Test your knowledge about SQLAlchemy.", "script")
book2 = Book("Test 5", "Test your knowledge about SQLAlchemy.", "script")
books = [book1, book2]
# db.session.bulk_save_objects(books)
