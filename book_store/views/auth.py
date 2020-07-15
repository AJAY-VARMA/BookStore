from flask_restful import Resource,Api
from flask import make_response,render_template,request,jsonify,redirect,url_for,session
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from services.db_services import DataBase
from services.mail_service import MailService
import os,jwt
from services.response import get
from flask_jwt_extended import create_access_token

class Login(Resource):

    def get(self):
        # return make_response(jsonify({"respone" : "get request called for login"}),200)
        return get,200

    def post(self):
        form = LoginForm(request.form)
        user_name = form.username.data
        password = form.password.data
        if form.validate():
            present_in_db =  DataBase.check_user_in_db(user_name,password)
            if present_in_db:
                access_token = create_access_token(identity=user_name)
                return make_response(jsonify({"respone" : access_token}),200)
            return make_response(jsonify({"respone" : "login failed"}),401)
        return make_response(jsonify({"respone" : form.username.errors+form.password.errors }),400)

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
        DataBase.check_token(token)
        return make_response(jsonify({"respone" : "login sucessfull"}),200)






class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=8, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm')

class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=8, max=50)])