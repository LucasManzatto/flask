from main.util.utils import success, created, message, conflict


class GenericTests:
    def __init__(self, endpoint, model, model_schema):
        self.endpoint = endpoint
        self.model = model
        self.model_schema = model_schema

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

    def insert(self, db_session, test_client, data, existing=False):
        object_json = self.model_schema.dump(data)
        key = list(filter(lambda x: x != 'id', (*object_json,)))[0]
        response = test_client.post(f'/{self.endpoint}/', json=object_json)
        if existing:
            assert conflict(response)
        else:
            assert created(response)
            assert message(response, "Author successfully created.")
        assert db_session.query(self.model).filter_by(name=object_json[key]).first()
        assert db_session.query(self.model).filter_by(name=object_json[key]).count() == 1

    def delete(self, db_session, test_client, id, has_fk=False):
        response = test_client.delete(f'/{self.endpoint}/{id}')
        db_data = db_session.query(self.model).get(id)
        if has_fk:
            assert conflict(response)
            assert not db_data
        else:
            assert success(response)
            assert not db_data
