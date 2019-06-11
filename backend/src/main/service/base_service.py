from backend.src.main import db
from backend.src.main.service import utils
from backend.src.main.util.utils import response_success, response_conflict, response_created, response_bad_request
from marshmallow import ValidationError


class BaseService:

    def __init__(self, model, model_name, schema, filter_by, filter_by_key, fks):
        self.model = model
        self.schema = schema
        self.filter_by = filter_by
        self.filter_by_key = filter_by_key
        self.fks = fks
        self.model_name = model_name

    def upsert(self, data, update):
        fk_objects = self.get_fk(data, self.fks)
        try:
            new_item = self.schema.load(data)
        except ValidationError as err:
            return response_bad_request(err.messages)

        item = self.model.query.filter(self.filter_by == data[self.filter_by_key]).first()
        if not item or update:
            return self.update_item(data, fk_objects) if update else self.create(new_item, fk_objects)
        else:
            return response_conflict(f'{self.model_name} already exists. Please choose another value.')

    @staticmethod
    def get_fk(data, fks):
        fk_objects = []
        for fk in fks:
            print(fk)
            ids = data.pop(fk['attr_name'], [])
            items = fk['fk_model'].query.filter(fk['fk_model'].id.in_(ids)).all()
            fk_objects.append({'key': fk['key'], 'value': items})
        return fk_objects

    def create(self, data, fks):
        del data.id
        for fk in fks:
            setattr(data, fk['key'], fk['value'])
        db.session.add(data)
        db.session.commit()
        return response_created(f'${self.model_name} successfully created.')

    def update_item(self, data, fks):
        item = self.model.query.get(data['id'])
        for fk in fks:
            setattr(item, fk['key'], fk['value'])
        self.model.query.filter_by(id=data['id']).update(data)
        db.session.commit()
        return response_success(f'${self.model_name} successfully updated.')

    def get_all(self, args):
        page = args.pop('page', 0)
        page_size = int(args.pop('per_page', 10))
        sort_query = utils.get_sort_query(args, self.model)
        sub_queries = utils.get_query(self.model, args)
        query_filter = self.model.query.filter(*sub_queries).order_by(sort_query).paginate(page=page, error_out=False,
                                                                                           max_per_page=page_size)
        return query_filter

    def get_one(self, id):
        return self.model.query.get_or_404(id)

    def get_model_fk(self, genre_id, fk):
        item = self.model.query.get(genre_id)
        return getattr(item, fk)

    def delete(self, id, *args):
        item = self.model.query.get(id)
        if item:
            for arg in args:
                setattr(item, arg['key'], [])
            self.model.query.filter_by(id=id).delete()
            db.session.commit()
            return response_success('')
        else:
            return response_bad_request(f'${self.model_name} not found.')
