
from flask_restplus import Api
from flask import Blueprint

from .main.controller.book_controller import api as book_ns
from .main.controller.author_controller import api as author_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(book_ns, path='/books')
api.add_namespace(author_ns, path='/authors')
