from backend.src.entities.entity import Book, db

# generate database schema
db.drop_all()
db.create_all()

# check for existing data
# books = Book.query.all()
# create and persist dummy exam
book1 = Book("Test 4", "Test your knowledge about SQLAlchemy.", "script")
book2 = Book("Test 5", "Test your knowledge about SQLAlchemy.", "script")
books = [book1, book2]
db.session.bulk_save_objects(books)
# db.session.add(book2)
db.session.commit()
# reload exams
books = Book.query.all()

# show existing exams
print('### Exams:')
for book in books:
    print(f'({book.id}) {book.title} - {book.description}')
