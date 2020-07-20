from flask_restful import Resource
from flask import request,jsonify,make_response
from services.db_services import DataBase
from flask_jwt_extended import jwt_required,get_jwt_identity
from services.response import *
from flask_restful_swagger import swagger

class Cart(Resource):
    swagger.operation(notes = 'get cart',parameters = [
            {
              "name": "Authorization",
              "description": "jwt token for the wishlist",
              "required": True,
              "type": "string",
              "paramType": "header"
            }]
            )
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        books_in_cart = DataBase.display_cart(user_name)
        return make_response(jsonify({"respone" : books_in_cart}),200)

    @jwt_required
    def post(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        DataBase.add_to_cart(user_name,product_id)
        return make_response(cart[200],200)

    @jwt_required
    def put(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = int(data['productid'])
        quantity = int(data['quantity'])
        books_in_cart,status_code = DataBase.update_cart(user_name,product_id,quantity)
        return make_response(jsonify({"respone" : books_in_cart}),status_code)

class Wishlist(Resource):
    @swagger.operation(notes = 'get wishlist',parameters = [
            {
              "name": "Authorization",
              "description": "jwt token for the wishlist",
              "required": True,
              "type": "string",
              "paramType": "header"
            }]
            )
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        books_data = DataBase.display_wishlist(user_name)
        return make_response(jsonify({"respone" : books_data}),200)

    @swagger.operation(notes = 'post wishlist',parameters = [
            {
              "name": "Authorization",
              "description": "jwt token for the wishlist",
              "required": True,
              "type": "string",
              "paramType": "header"
            },{
              "name": "productid",
              "description": "product id to add to wishlist",
              "required": True,
              "type": "string",
              "paramType": "form"
            }]
            )
    @jwt_required
    def post(self):
        data = request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        msg = DataBase.add_to_wishlist(user_name,product_id)
        return make_response(msg,200)