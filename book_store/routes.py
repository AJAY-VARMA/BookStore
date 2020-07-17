from flask import Flask
from flask_restful import Api
from views import Login,Register,RegisterEmail,GetBooks,Sort,Cart,Wishlist,Order,CheckOut
from app import app
from flask_jwt_extended import  JWTManager

api = Api(app)
jwt = JWTManager(app)

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(RegisterEmail , '/register-email/<token>')
api.add_resource(GetBooks,'/getbooks')
api.add_resource(Sort,'/getbooks/sort-by-price')
api.add_resource(Cart,'/getbooks/add-to-cart')
api.add_resource(Wishlist,'/getbooks/add-to-wishlist')
api.add_resource(Order,'/getbooks/add-to-cart/order')
api.add_resource(CheckOut,'/getbooks/add-to-cart/checkout')
