from flask_restful import Resource
from flask import make_response,request,redirect,url_for,jsonify
import jinja2,jwt,os
from .mail import MailService
from .db import DataBase
from wtforms import Form,StringField,PasswordField,validators
from dotenv import load_dotenv

class Register(Resource):
    def get(self):
        return make_response(jsonify({"respone" : "get request called for register"}),200)

    def post(self):
            form = RegisterForm(request.form)
            user_name = form.username.data
            email =  form.email.data
            password = form.password.data
            if form.validate():
                mail_msg = MailService.send_mail(user_name,email)
                return DataBase.add_to_db(user_name,email,password,mail_msg)
            return make_response(jsonify({"respone" : "enter proper details for registration"}),400)
        
class RegisterEmail(Resource):
    def get(self,token):
       return make_response(jsonify({"respone" : "login sucessfull"}),200)
    
class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=8, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm')


