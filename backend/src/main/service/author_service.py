from backend.src.main import db
from main.model.author import Author, AuthorSchema


def create_author(data):
    author = Author.query.filter_by(name=data['name']).first()
    if not author:
        new_author = AuthorSchema().load(data).data
        save_changes(new_author)
        response_object = {
            'status': 'success',
            'message': 'Author successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Author already exists. Please choose another name.',
        }
        return response_object, 409


def update_author(author):
    Author.query.filter_by(id=author['id']).update(author)
    db.session.commit()
    return None, 201


def get_all_authors():
    return Author.query.all()


def get_an_author(author_id):
    return Author.query.get_or_404(author_id)


def delete_author(author_id):
    Author.query.filter_by(id=author_id).delete()
    db.session.commit()
    return None, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
