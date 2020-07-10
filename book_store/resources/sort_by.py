from flask_restful import Resource
from flask import request,jsonify,make_response
from .db import DataBase

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
        

            