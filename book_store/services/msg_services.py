from twilio.rest import Client,TwilioException
from dotenv import load_dotenv
import os
from .error_handler_service import InvalidUsageError
from .response import twilio
import asyncio
# account_sid = os.getenv('account_sid')
# auth_token = os.getenv('auth_token')
# mobile_num = os.getenv("mobilenum")

account_sid = 'ACa1ebf0723be29374c248fd663672a65b'
auth_token = '041555e4619d9d1ba10cf9cba3164cfc'
mobile_num = '+19387777591'

class MsgService():
    @staticmethod
    async def send_message(details):
        try:
            await asyncio.sleep(10)
            client = Client(account_sid, auth_token)
            message = ( client.messages \
                .create(
                    body='your order id :{} with total price:{}'.format(details[0],details[2]),
                    from_=mobile_num,
                    to='+91'+str(details[1])
                ))
        except TwilioException:
            raise InvalidUsageError(twilio[500],500)



