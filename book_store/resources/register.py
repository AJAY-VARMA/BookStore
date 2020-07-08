from flask_restful import Resource
from flask import make_response,render_template,request,g,redirect,url_for,jsonify
import jinja2,jwt,os
from .mail import MailService
from .db import DataBase
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from .error_handler import InvalidUsageError
load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')
mail_user = os.getenv('mail_user')

class Register(Resource):
    def get(self):
        return make_response(jsonify({"respone" : "get request called for register"}),200)
        # try:
        #     return make_response(render_template('registration.html'))
        # except jinja2.exceptions.TemplateNotFound:
        #     raise InvalidUsageError("template not found",404)


    def post(self):
        # try:
            form = RegisterForm(request.form)
            user_name = form.username.data
            email =  form.email.data
            password = form.password.data
            if form.validate():
                DataBase.add_to_db(user_name,email,password)
                token = jwt.encode({'user_name':user_name,'email':email,'password':password}
                    ,secret_key).decode('utf-8')
                msg = MailService.send_mail(token,email,mail_user)
                return make_response(jsonify({"respone" : msg}),200)
            return make_response(jsonify({"respone" : "registration failed"}),401)
        # except Exception:
        #     raise InvalidUsageError("requesting from form error",500)

class RegisterEmail(Resource):
    def get(self,token):
        # data = jwt.decode(token,secret_key)
        # return DataBase.add_to_db(data)
       return make_response(jsonify({"respone" : "login sucessfull"}),200)
    
class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=8, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm')


