
from flask import Blueprint
from flask_restplus import Api

from backend.src.main.controller.genre_controller import api as genres_ns
from backend.src.main.controller.book_controller import api as book_ns
from backend.src.main.controller.author_controller import api as author_ns
from backend.src.main.controller.series_controller import api as series_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK',
          version='1.0',
          )

api.add_namespace(book_ns, path='/books')
api.add_namespace(author_ns, path='/authors')
api.add_namespace(series_ns, path='/series')
api.add_namespace(genres_ns, path='/genres')
