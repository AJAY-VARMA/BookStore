from flask import Flask,jsonify
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv('bookenv/.env')

app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['MAIL_PORT'] = os.getenv("mail_port")
app.config['MAIL_USERNAME'] = os.getenv("mail_user")
app.config['MAIL_PASSWORD'] = os.getenv("mail_pswd")
app.config['MAIL_USE_SSL'] = True
app.config['secret_key'] = os.getenv("secret_key")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("connection")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# @app.errorhandler(InvalidUsageError)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response