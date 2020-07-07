from flask_restful import Resource,Api
from flask import make_response,render_template,request
import jinja2
from .db import DataBase

class Login(Resource):
    def get(self):
        try:
            return make_response(render_template('login.html'))
        except jinja2.exceptions.TemplateNotFound:
            pass

    def post(self):
        # try:
            user_details = request.form
            user_name = user_details['name']
            password = user_details['pswd']
            return DataBase.check_user_in_db(user_name,password)
        # except Exception:
        #     pass


