from flask import Flask,jsonify
from dotenv import load_dotenv
import os
from services.error_handler_service import InvalidUsageError
from model.model import db
from services.mail_service import mail
from routes import initialize_routes
from flask_jwt_extended import  JWTManager
from flask_restful_swagger import swagger
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
initialize_routes(api)
jwt = JWTManager(app)
api = swagger.docs(Api(app),apiVersion='3.0',api_spec_url='/docs')
load_dotenv('bookenv/.env')

app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['MAIL_PORT'] = os.getenv("mail_port")
app.config['MAIL_USERNAME'] = os.getenv("mail_user")
app.config['MAIL_PASSWORD'] = os.getenv("mail_pswd")
app.config['MAIL_USE_SSL'] = True
app.config['secret_key'] = os.getenv("secret_key")
app.config['JWT_SECRET_KEY'] = os.getenv("jwt_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("connection")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail.init_app(app)
db.init_app(app)

@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
