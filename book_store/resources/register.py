from flask_restful import Resource
from flask import make_response,render_template,request,g,redirect,url_for
import jinja2,jwt,os
from .mail import MailService
from .db import DataBase
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')
mail_user = os.getenv('mail_user')

class Register(Resource):
    def get(self):
        try:
            return make_response(render_template('registration.html'))
        except jinja2.exceptions.TemplateNotFound:
            pass

    def post(self):
        try:
            # form = RegisterForm(request.form)
            user_details = request.form
            user_name = user_details['name']
            email =  user_details['email']
            password = user_details['pswd']
            re_password = user_details['pswd1']
            # if form.validate():
            #     return "true"
            token = jwt.encode({'user_name':user_name,'email':email,'password':password}
                ,secret_key).decode('utf-8')
            return MailService.send_mail(token,email,mail_user)
        except Exception:
            pass

class RegisterEmail(Resource):
    def get(self,token):
        data = jwt.decode(token,secret_key)
        return DataBase.add_to_db(data)
    
# class RegisterForm(Form):
#     username = StringField('name', [validators.Length(min=4, max=25)])
#     email = StringField('email', [validators.Length(min=6, max=50)])
#     password = PasswordField('pswd', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')
#     ])
#     confirm = PasswordField('pswd1')


