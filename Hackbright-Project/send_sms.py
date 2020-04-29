# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from model import User, Event


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_API_KEY']
client = Client(account_sid, auth_token)


def send_message(user_name, phone, event_name, event_time, event_date, event_venue, event_lat, event_lng):

    print(user_name, phone, event_name, event_time, event_date)
    

    message = client.messages \
                    .create(
                         body=f"Hi { user_name }, You have an event coming up soon! {event_name}, {event_date}, {event_time}",
                         from_='+12058462350',
                         to=phone
                     )


    print(message.sid)

