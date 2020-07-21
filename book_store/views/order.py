from flask_restful import Resource
from services.db_services import DataBase
from services.mail_service import MailService
from flask import make_response,request,jsonify
from services.response import *
from flask_login import login_required
from flask_jwt_extended import jwt_required,get_jwt_identity

class Order(Resource):
    @jwt_required
    def get(self):
        return make_response(order[200],200)
    
    @jwt_required
    def post(self):
        customer = request.form
        username = get_jwt_identity()
        mobile_number = customer['mobilenumber']
        address = customer['address']
        DataBase.add_to_order_db(username,mobile_number,address)
        return make_response(order_post[200],200)

class CheckOut(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        DataBase.change_products_quantity_in_db()
        user_details,product_details = DataBase.get_user_details(username)
        MailService.send_mail_with_order_details(user_details,product_details)
        return make_response(checkout[200],200)
