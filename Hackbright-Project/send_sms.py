# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_API_KEY']
client = Client(account_sid, auth_token)


def send_message(phone_number)
    message = client.messages \
                    .create(
                         body="You have an event tonight!",
                         from_='+12058462350',
                         to=phone_number
                     )


    print(message.sid)

