from flask_mail import Message,Mail
import sys,os
sys.path.append('.')
from app import app

from .error_handler import InvalidUsageError
mail = Mail(app)

class MailService:
    @staticmethod 
    def send_mail(token,email,mail_user):
        try:
            msg = Message( 
                    'Hello', 
                    sender = mail_user, 
                    recipients = [email]
                ) 
            msg.body = '''verification link : click the link for registration
            http://127.0.0.1:5000/register-email/{}'''.format(token)
            mail.send(msg)
            return "check your mail click the link for verification"
        except:
           pass