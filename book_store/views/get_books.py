from flask_restful import Resource
from services.db_services import DataBase
from flask import make_response,request,jsonify
from flask_login import login_required
from services.response import *
from flask_restful_swagger import swagger
from swag import search,sort

class GetBooks(Resource):

    @swagger.operation(notes = 'get books')
    def get(self):
        books_data = DataBase.get_books_data_from_db()
        return make_response(jsonify({"books" : books_data}),200)

    @swagger.operation(notes = 'search books',parameters = search)
    def post(self):
        search_value = request.args.get('search')
        product_data = DataBase.search_book(search_value)
        if len(product_data) > 0:
            return make_response(jsonify({"books" : product_data}),200)
        return make_response(search_response[400],400)

class Sort(Resource):
    @swagger.operation(notes = 'get sort')
    def get(self):
        return make_response(sort[200],200)

    @swagger.operation(notes = 'post sort',parameters = sort)
    def post(self):
        data = request.args.get('sort')
        data = data.lower()
        if data ==  "lowtohigh":
            value = True
        elif data == "hightolow":
            value = False
        else:
            return make_response(sort[400],400)
        sorted_books = DataBase.sort_books_by_price(value)
        return make_response(jsonify({"respone" : sorted_books}),200)