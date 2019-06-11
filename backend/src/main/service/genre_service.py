from backend.src.main.model.genre import GenreSchema, Genre
from backend.src.main.model.books import Book
from backend.src.main.service.base_service import BaseService


class GenreService(BaseService):
    def __init__(self):
        fks = [{'key': 'books', 'attr_name': 'books_ids', 'fk_model': Book}]
        super().__init__(model=Genre, model_name='Genre', schema=GenreSchema(), filter_by=Genre.name,
                         filter_by_key='name', fks=fks)

    @staticmethod
    def get_genre_books(genre_id):
        books = Genre.query.get(genre_id).books
        return books
