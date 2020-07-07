from flask import Flask
from flask_restful import Api
from resources import register,login,db
import os

from app import app

api = Api(app)

api.add_resource(login.Login,'/login')
api.add_resource(register.Register,'/register')
api.add_resource(register.RegisterEmail , '/register-email/<token>')