from flask_restful import Resource
from flask import make_response,render_template,request,g
import jinja2,jwt,os
from dotenv import load_dotenv
from .mail import MailService
from .db import DataBase
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
        # try:
            user_details = request.form
            user_name = user_details['name']
            email =  user_details['email']
            password = user_details['pswd']
            token = jwt.encode({'user_name':user_name,'email':email}
                ,secret_key).decode('utf-8')
            return MailService.send_mail(token,email,mail_user)
        # except Exception:
        #     pass

class RegisterEmail(Resource):
    def get(self,token):
        data = jwt.decode(token,secret_key)
        return DataBase.add_to_db(data)