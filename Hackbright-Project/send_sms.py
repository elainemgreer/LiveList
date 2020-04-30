import os
from twilio.rest import Client
from model import User, Event


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_API_KEY']
client = Client(account_sid, auth_token)


def send_message(user, event):
    """Sends message to user with event details."""
    

    message = client.messages \
                    .create(
                         body=f"Hi { user.name }, You have an event coming up soon! { event.event_name }, {event.event_date}, { event.event_time}",
                         from_='+12058462350',
                         to=user.phone
                     )


    print(message.sid)

