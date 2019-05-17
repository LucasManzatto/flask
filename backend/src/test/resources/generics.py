from main.model.author import Author
from main.util.utils import success, created, message, conflict, not_found


class GenericTests:
    def __init__(self, endpoint, model, model_schema, filter_by, filter_by_key):
        self.endpoint = endpoint
        self.model = model
        self.model_schema = model_schema
        self.filter_by = filter_by
        self.filter_by_key = filter_by_key

    def get_one(self, test_client, db_session):
        object_from_db = db_session.query(self.model).first()
        response = test_client.get(f'/{self.endpoint}/{object_from_db.id}')
        assert success(response)
        assert response.json['id'] == object_from_db.id

    def get_all(self, test_client, db_session):
        table_row_size = db_session.query(self.model).count()
        response = test_client.get(f'/{self.endpoint}/')
        response_size = len(response.json[self.endpoint])
        assert success(response)
        assert table_row_size == response_size

    def get_not_found(self, test_client):
        response = test_client.get(f'/{self.endpoint}/-1')
        assert not_found(response)

    def insert(self, db_session, test_client, data=None, json_data=None, existing=False, update=False):
        if json_data is None:
            json_data = {}
        if existing:
            data = db_session.query(self.model).first()

        if data:
            object_json = self.model_schema.dump(data)
        else:
            object_json = json_data

        if update:
            response = test_client.put(f'/{self.endpoint}/', json=object_json)
        else:
            response = test_client.post(f'/{self.endpoint}/', json=object_json)
        print(response)
        created_object = db_session.query(self.model).filter(self.filter_by == object_json[self.filter_by_key]).first()
        only_one_created = db_session.query(self.model).filter(
            self.filter_by == object_json[self.filter_by_key]).count() == 1
        if existing:
            assert conflict(response)
        else:
            assert success(response) if update else created(response)
        assert created_object
        assert only_one_created

    def delete(self, db_session, test_client, id, has_fk=False):
        response = test_client.delete(f'/{self.endpoint}/{id}')
        db_data = db_session.query(self.model).get(id)
        if has_fk:
            assert conflict(response)
            assert db_data
        else:
            assert success(response)
            assert not db_data
