from flask_restful import Resource
from .db import DataBase
from flask import make_response,render_template,request,jsonify
from .error_handler import InvalidUsageError
import jinja2

class GetBooks(Resource):
    def get(self):
        product_data = DataBase.get_data_from_db()
        return make_response(jsonify({"books" : product_data}),200)
        # try:
        #     product_data = DataBase.get_data_from_db()
        #     return make_response(render_template('get_books.html',product_data = product_data))
        # except jinja2.exceptions.TemplateNotFound:
        #     raise InvalidUsageError("template not found",404)

    def post(self):
        # try:
            book_data = request.form
            book_id = book_data['search']
            product_data = DataBase.get_book_data_by_id(book_id)
            return make_response(jsonify({"books" : product_data}),200)
            # return make_response(render_template('get_books.html',product_data = product_data))
        # except jinja2.exceptions.TemplateNotFound:
        #     raise InvalidUsageError("template not found",404)