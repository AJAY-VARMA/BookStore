from flask_mail import Message,Mail
from app import app
# from book_store.app  import app
from .error_handler import InvalidUsageError
import os,jwt
from dotenv import load_dotenv

load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')
mail_user = os.getenv('mail_user')

mail = Mail(app)

class MailService:
    @staticmethod 
    def send_mail(user_name,email):
        try:
            token = jwt.encode({'user_name':user_name,'email':email}
                    ,secret_key).decode('utf-8')
            msg = Message( 
                    'Hello', 
                    sender = mail_user,
                    recipients = [email]
                ) 
            msg.body = '''verification link : click the link for registration
            http://127.0.0.1:5000/register-email/{}'''.format(token)
            mail.send(msg)
            return "check your mail click the link for verification"
        except (NameError,AssertionError):
           raise InvalidUsageError('error in mail service', 500)