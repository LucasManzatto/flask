from backend.src.main import db
from backend.src.main.model.entity import Entity


class Author(Entity, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(30))

    def __init__(self, title, description, last_updated_by):
        self.title = title
        self.description = description
        self.last_updated_by = last_updated_by

    def __repr__(self):
        return f"Book:{self.title}"
