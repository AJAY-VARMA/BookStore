from flask import Flask
from flask_restful import Api
from resources import Login,Register,RegisterEmail,GetBooks
import os

from app import app

api = Api(app)

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(RegisterEmail , '/register-email/<token>')
api.add_resource(GetBooks,'/getbooks')