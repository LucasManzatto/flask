from backend.src.main.model.series import Series, SeriesSchema
from backend.src.main.model.books import Book
from main.service.base_service import BaseService


class SeriesService(BaseService):
    def __init__(self):
        fks = [{'key': 'books', 'attr_name': 'books_ids', 'fk_model': Book}]
        super().__init__(model=Series, model_name='Series', schema=SeriesSchema(), filter_by=Series.title,
                         filter_by_key='title', fks=fks)
