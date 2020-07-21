from flask_mail import Message,Mail
from flask import render_template
from .error_handler_service import InvalidUsageError
import os,jwt
from dotenv import load_dotenv

load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')
mail_user = os.getenv('mail_user')
host = os.getenv('host')
mail = Mail()
class MailService:

    @staticmethod
    def send_mail_with_order_details(user_details,product_details):
        products = product_details[:-1]
        price = product_details[-1]
        msg = Message( 
                    'From Books Store', 
                    sender = mail_user,
                    recipients = [user_details[0]]
                ) 
        msg.html = render_template('email.html',user = user_details,products = products,price = price)
        mail.send(msg)

    @staticmethod 
    def send_mail_with_link(user_name,email):
        try:
            token = jwt.encode({'email':email}
                    ,secret_key).decode('utf-8')
            msg = Message( 
                    'Hello', 
                    sender = mail_user,
                    recipients = [email]
                ) 
            msg.body = '''verification link : click the link for registration
            {}'''.format((host+token))
            mail.send(msg)
            return "check your mail click the link for verification"
        except (NameError,AssertionError):
           raise InvalidUsageError('error in mail service', 500)