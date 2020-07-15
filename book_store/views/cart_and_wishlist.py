from flask_restful import Resource
from flask import request,jsonify,make_response
from services.db_services import DataBase
from flask_jwt_extended import jwt_required,get_jwt_identity

class Cart(Resource):
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        price = 0
        books_in_cart,price = DataBase.display_cart(user_name)
        return price
        return make_response(jsonify({"respone" : books_in_cart}),200)

    @jwt_required
    def post(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        DataBase.add_to_cart(user_name,product_id)
        return make_response(jsonify({"respone" : "added to cart"}),200)

class Wishlist(Resource):
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        obj = DataBase.display_wishlist(user_name)
        return make_response(jsonify({"respone" : obj}),200)

    @jwt_required
    def post(self):
        data = request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        DataBase.add_to_wishlist(user_name,product_id)
        return make_response(jsonify({"respone" : "added to wishlist"}),200)