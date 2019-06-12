from backend.src.main.model.author import Author, AuthorSchema
from backend.src.main.model.series import Series
from backend.src.main.service.base_service import BaseService
from marshmallow import INCLUDE


class AuthorService(BaseService):
    def __init__(self):
        fks = [{'key': 'series', 'attr_name': 'series_ids', 'fk_model': Series}]
        dependencies = ['books', 'series']
        super().__init__(model=Author, model_name='Author', schema=AuthorSchema(unknown=INCLUDE), filter_by=Author.name,
                         filter_by_key='name', fks=fks, dependencies=dependencies)
