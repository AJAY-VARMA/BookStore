from flask_restful import Resource
from flask import request,jsonify,make_response
from services.db_services import DataBase
from flask_jwt_extended import jwt_required,get_jwt_identity
from services.response import *
from flask_restful_swagger import swagger
from swag import jwt,product,quantity
from redis.exceptions import ConnectionError
# from decorator import check_token
from flask_redis import FlaskRedis
# from app import app
redis = FlaskRedis()

class Cart(Resource):
    @swagger.operation(notes = 'get cart',parameters = jwt)
    @jwt_required
    def get(self):
        try:
            user_name = get_jwt_identity()
            if redis.exists(user_name):
                books_in_cart = DataBase.display_cart(user_name)
                return make_response(jsonify({"respone" : books_in_cart,"status" : 200}),200)
            return make_response(login_response[413],413)
        except ConnectionError :
            raise InvalidUsageError(redis_error[500],500)
            
     
    @swagger.operation(notes = 'post cart',parameters = product)
    @jwt_required
    def post(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        return DataBase.add_to_cart(user_name,product_id)

    @swagger.operation(notes = 'delete cart',parameters = product)
    @jwt_required
    def delete(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        DataBase.remove_from_cart(user_name,product_id)
        return make_response(response['deleted'],200)

    @swagger.operation(notes = 'put cart',parameters = quantity)
    @jwt_required
    def put(self):
        data =  request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        quantity = data['quantity']
        books_in_cart,status_code = DataBase.update_cart(user_name,product_id,quantity)
        return make_response(jsonify({"respone" : books_in_cart}),status_code)

class Wishlist(Resource):
    @swagger.operation(notes = 'get wishlist',parameters = jwt)
    @jwt_required
    def get(self):
        user_name = get_jwt_identity()
        books_data = DataBase.display_wishlist(user_name)
        return make_response(jsonify({"respone" : books_data,"status" : 200}),200)

    @swagger.operation(notes = 'post wishlist',parameters = product)
    @jwt_required
    def post(self):
        data = request.form
        user_name = get_jwt_identity()
        product_id = data['productid']
        response = DataBase.add_to_wishlist(user_name,product_id)
        return make_response(response,200)