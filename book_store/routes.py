from flask import Flask
from flask_restful import Api
from views import Login,Register,RegisterEmail,GetBooks,Sort,Cart,Wishlist
import os
from app import app
from flask_login import LoginManager
from flask_jwt_extended import  JWTManager

api = Api(app)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(RegisterEmail , '/register-email/<token>')
api.add_resource(GetBooks,'/getbooks')
api.add_resource(Sort,'/getbooks/sort-by-price')
api.add_resource(Cart,'/getbooks/add-to-cart')
api.add_resource(Wishlist,'/getbooks/add-to-wishlist')
