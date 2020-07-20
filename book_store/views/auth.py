from flask_restful import Resource
from flask import make_response,request,jsonify
from services.db_services import DataBase
from services.mail_service import MailService
from services.response import *
from flask_jwt_extended import create_access_token
from form import RegisterForm,LoginForm
from flasgger.utils import swag_from
from flask_restful_swagger import swagger

class Login(Resource):
    
    @swagger.operation(notes = 'get login page')
    def get(self):
        return make_response(get_login[200],200)

    @swagger.operation(notes = 'post login page',parameters = [
            {
              "name": "username",
              "description": "enter username for the login",
              "required": True,
              "type": "string",
              "paramType": "form"
            },
            {
              "name": "password",
              "description": "enter password for the login",
              "required": True,
              "type": "string",
              "paramType": "form"
            }
          ])
    def post(self):
        form = LoginForm(request.form)
        user_name = form.username.data
        password = form.password.data
        if form.validate():
            present_in_db =  DataBase.check_user_in_db(user_name,password)
            if present_in_db:
                access_token = create_access_token(identity=user_name)
                return make_response(jsonify({"respone" : access_token}),200)
            return make_response(failed_login[401],401)
        return make_response(jsonify({"respone" : form.username.errors+form.password.errors }),400)

class Register(Resource):
    def get(self):
        return make_response(get_register[200],200)

    def post(self):
            form = RegisterForm(request.form)
            user_name = form.username.data
            email =  form.email.data
            password = form.password.data
            if form.validate():
                mail_msg = MailService.send_mail_with_link(user_name,email)
                return DataBase.add_user_to_db(user_name,email,password,mail_msg)
            return make_response(validation_msg[400],400)
        
class RegisterEmail(Resource):
    def get(self,token):
        DataBase.check_token(token)
        return make_response(login[200],200)



