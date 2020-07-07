from flask import Flask
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv('bookenv/.env')

app.config['MAIL_SERVER'] = os.getenv("mail_server")
app.config['MAIL_PORT'] = os.getenv("mail_port")
app.config['MAIL_USERNAME'] = os.getenv("mail_user")
app.config['MAIL_PASSWORD'] = os.getenv("mail_pswd")
app.config['MAIL_USE_SSL'] = True

