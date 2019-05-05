from backend.src.db import db


class Entity(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_updated_by = db.Column(db.String(30))


