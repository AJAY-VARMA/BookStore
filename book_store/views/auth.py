from flask_restful import Resource
from flask import make_response,request,jsonify
from services.db_services import DataBase
from services.response import *
from flask_jwt_extended import create_access_token
from form import RegisterForm,LoginForm
from flask_restful_swagger import swagger
from swag import login,register,token
from flask import current_app as app
from flask_redis import FlaskRedis
from redis.exceptions import ConnectionError
from services.error_handler_service import InvalidUsageError

reddis = FlaskRedis()

# def check_token(func):
#     redi   redi.set(name = "xyx",value = "xyz")
#     return func

class Login(Resource):

    @swagger.operation(notes = 'post login page',parameters = login)
    def post(self):
        form = LoginForm(request.form)
        user_name = form.username.data
        password = form.password.data
        try :
            if not form.validate():
                return make_response(login_response[400],400)
            present_in_db,confirmed =  DataBase.check_user_in_db(user_name,password)
            if present_in_db :
                if not confirmed:
                    return make_response(login_response[411],411)
                access_token = create_access_token(identity=user_name)
                # app.logger.info('{} was logged in'.format(user_name))
                reddis.set(name = user_name,value = access_token)
                reddis.expire(user_name ,(23*60*60))
                return make_response(jsonify({"respone:token" : access_token,"status": 200}),200)
            return make_response(login_response[401],401)
            # app.logger.error(form.username.errors+form.password.errors)        
        except ConnectionError:
            raise InvalidUsageError(redis_error[500],500)


class Register(Resource):
    @swagger.operation(notes = 'post registration page',parameters = register)
    def post(self):
            form = RegisterForm(request.form)
            user_name = form.username.data
            email =  form.email.data
            password = form.password.data
            if form.validate():
                return DataBase.add_user_to_db(user_name,email,password)
            return make_response(registration_response[400],400)
       
class RegisterEmail(Resource):
    @swagger.operation(notes = 'get register email',parameters = token)
    def get(self,token):
        DataBase.check_token(token)
        return make_response(registration_response["success"],200)



