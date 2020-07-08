from flask import Flask,jsonify
from dotenv import load_dotenv
from resources.error_handler import InvalidUsageError
# from .resources.error_handler import InvalidUsageError
import os
app = Flask(__name__)

load_dotenv('bookenv/.env')

app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['MAIL_PORT'] = os.getenv("mail_port")
app.config['MAIL_USERNAME'] = os.getenv("mail_user")
app.config['MAIL_PASSWORD'] = os.getenv("mail_pswd")
app.config['MAIL_USE_SSL'] = True

# app.config['MYSQL_HOST'] = os.getenv("sql_host")
# app.config['MYSQL_USER'] = os.getenv("sql_user")
# app.config['MYSQL_PASSWORD'] = os.getenv("sql_pswd")
# app.config['MYSQL_DB'] = os.getenv("sql_db")
# app.config['secret_key'] = os.getenv("secret_key")

# c = os.getenv("sql_host")
# print(c)


app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "1234"
app.config['MYSQL_DB'] = "bookstore"
app.config['secret_key'] = "secretkey"

@app.errorhandler(InvalidUsageError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response