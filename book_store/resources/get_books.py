from flask_restful import Resource
from .db import DataBase
from flask import make_response,render_template,request,jsonify
from .error_handler import InvalidUsageError
import jinja2

class GetBooks(Resource):
    def get(self):
        product_data = DataBase.get_data_from_db()
        return make_response(jsonify({"books" : product_data}),200)

    def post(self):
            book_form = request.form
            search_value = book_form['search']
            product_data = DataBase.search_book(search_value)
            if len(product_data) > 0:
                return make_response(jsonify({"books" : product_data}),200)
            return make_response(jsonify({"response":"the book u typed is not available"}),400)