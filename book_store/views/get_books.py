from flask_restful import Resource
from services.db_services import DataBase
from flask import make_response,render_template,request,jsonify
import jinja2
from flask_login import login_required

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

class Sort(Resource):
    def get(self):
        return make_response(jsonify({"respone" : "get request called for sort"}),200)

    def post(self):
        data = request.form['sort_by']
        data = data.lower()
        if data ==  "lowtohigh":
            value = True
        elif data == "hightolow":
            value = False
        else:
            return make_response(jsonify({"respone" : "enter correct values to sort"}),400)
        sorted_books = DataBase.sort_books_by_price(value)
        return make_response(jsonify({"respone" : sorted_books}),200)