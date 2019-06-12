from backend.src.main.model.author import Author
from backend.src.main.model.books import Book, BookSchema
from backend.src.main.model.series import Series
from backend.src.main.service import utils
from backend.src.main.service.base_service import BaseService
from backend.src.main.model.genre import Genre
from main.util.utils import response_bad_request, response_conflict
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload


class BookService(BaseService):
    author_fk = {'key': 'author', 'attr_name': 'author_id', 'fk_model': Author}
    series_fk = {'key': 'series', 'attr_name': 'series_id', 'fk_model': Series}
    genres_fk = {'key': 'genres', 'attr_name': 'genre_ids', 'fk_model': Genre}
    fks = [genres_fk]

    def __init__(self):
        super().__init__(model=Book, model_name='Book', schema=BookSchema(), filter_by=Book.title,
                         filter_by_key='title', fks=self.fks)

    def upsert(self, data, update):
        # genres = self.get_fk(data, self.genres_fk)
        ids = data.pop('genre_ids', [])
        genres = Genre.query.filter(Genre.id.in_(ids)).all()
        try:
            new_book = BookSchema().load(data)
            del new_book.author
        except ValidationError as err:
            print(err.messages)
            return response_bad_request(err.messages)

        book = Book.query.filter_by(title=data['title']).first()
        if not book or update:
            author = Author.query.filter(Author.id == new_book.author_id).first()
            series = Series.query.filter(Series.id == new_book.series_id).first()
            if author:
                if series or not new_book.series_id:
                    return self.update_item(data, [{'key': 'genres', 'value': genres}]) if update else self.create(
                        new_book,
                        [{'key': 'genres', 'value': genres}])
                elif new_book.series_id:
                    return response_bad_request("Series doesn't exist.")
            else:
                return response_bad_request("Author doesn't exist.")
        else:
            return response_conflict('Book already exists. Please choose another title.')

    def get_all(self, args):
        page = int(args.pop('page', 0))
        page_size = int(args.pop('per_page', 10))
        sort_query = utils.get_sort_query(args, Book)
        sub_queries = utils.get_query(Book, args)
        query_filter = Book.query.join(Author).options(joinedload('author')).filter(*sub_queries).order_by(
            sort_query).paginate(page=page,
                                 error_out=False,
                                 max_per_page=page_size)
        return query_filter
