from flask_restful import Resource
from .db import DataBase
from flask import make_response,render_template

class GetBooks(Resource):
    def get(self):
        try:
            product_data = DataBase.get_data_from_db()
            return make_response(render_template('get_books.html',product_data = product_data))
        except:
            pass
    def post(self):
        pass