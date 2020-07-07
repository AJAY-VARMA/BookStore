from flask_restful import Resource,Api
from flask import make_response,render_template
import jinja2 

class Login(Resource):
    def get(self):
        try:
            return make_response(render_template('login.html'))
        except jinja2.exceptions.TemplateNotFound:
            pass

    def post(self):
        pass

