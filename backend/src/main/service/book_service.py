from backend.src.main.model.author import Author
from backend.src.main.model.books import Book, BookSchema
from backend.src.main.model.genre import Genre
from backend.src.main.service.base_service import BaseService


class BookService(BaseService):
    genres_fk = {'key': 'genres', 'attr_name': 'genre_ids', 'fk_model': Genre}
    fks = [genres_fk]

    joins = [{'join_model': Author, 'joinedload': 'author'}]

    def __init__(self):
        super().__init__(model=Book, model_name='Book', schema=BookSchema(), filter_by=Book.title,
                         filter_by_key='title', fks=self.fks, joins=self.joins)

