from flask_restful import Resource,Api
from flask import make_response,render_template,request,jsonify,redirect,url_for
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
import jinja2
from .db import DataBase
from .error_handler import InvalidUsageError

class Login(Resource):

    def get(self):
        return make_response(jsonify({"respone" : "get request called for login"}),200)

    def post(self):
            form = LoginForm(request.form)
            user_name = form.username.data
            password = form.password.data
            if form.validate():
                return Login.check_db(user_name,password)
            return make_response(jsonify({"respone" : "enter proper values for validation"}),400)

    @staticmethod
    def check_db(user_name,password):
        present_in_db =  DataBase.check_user_in_db(user_name,password)
        if present_in_db:
            return make_response(jsonify({"respone" : "login success"}),200)
            # return redirect(url_for('getbooks'))
        return make_response(jsonify({"respone" : "login failed"}),401)

class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=8, max=50)])