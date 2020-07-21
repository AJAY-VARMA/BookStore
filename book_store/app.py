from flask import Flask,jsonify,send_from_directory
from dotenv import load_dotenv
import os
from services.error_handler_service import InvalidUsageError

app = Flask(__name__)
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

@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
