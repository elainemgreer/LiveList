import json
import requests
from pprint import pprint
import os
from geopy import distance
from model import User, UserEvent, Event
from datetime import datetime, date


api_key = os.environ['SK_KEY']



def get_metro_id_by_lat_lng(latitude, longitude):
    """Gets metro ID of user to use to find events"""


    request_string = (f'https://api.songkick.com/api/3.0/search/locations.json?location=geo:{latitude},{longitude}&apikey={api_key}')

    metro_id_results = requests.get(request_string)

    json = metro_id_results.json()


    location = json['resultsPage']['results']['location']
    city_dict = location[0]
    metro = city_dict['metroArea']
    metro_id = metro['id']

    return metro_id




def get_metro_id_by_city(city):
    """Uses city that user enters to find metro id of city."""


    request_string = (f'https://api.songkick.com/api/3.0/search/locations.json?query={city}&apikey={api_key}')

    metro_id_results = requests.get(request_string)

    json = metro_id_results.json()


    location = json['resultsPage']['results']['location']
    city_dict = location[0]
    metro = city_dict['metroArea']
    metro_id = metro['id']

    return metro_id




def get_events_list_by_metro_area_and_date(metro_id, min_date, max_date):
    """Uses metro ID and min/max dates to generate list of events."""

    metro_id = str(metro_id)

    

    payload = {'apikey': api_key,
            'metro_area_id': metro_id,
            'min_date': min_date,
            'max_date': max_date}


    events_json = requests.get('https://api.songkick.com/api/3.0/events.json',
            params=payload)


    events_json = events_json.json()

    
    # num_events = events_json['resultsPage']['totalEntries'] 
    # print("*************" num_events "******************")


    events_list = events_json['resultsPage']['results']['event']



    return events_list



# events_list = get_events_list_by_metro_area_and_date('9179', '2020-02-17', '2020-02-17')


def get_locations(events_list):



    event_locations = []

    for event in events_list:

        if event['venue']['lat'] and event['venue']['lng'] != None:

            event_location = []

            event_id = event['id']
            name = event['displayName']
            venue = event['venue']['displayName']
            lat = event['venue']['lat']
            lng = event['venue']['lng']
            date = event['start']['date']
            time = event['start']['time']
            url = event['uri']

            date = datetime.strptime(date, '%Y-%m-%d')
            
            date = date.strftime("%b %d %Y")

            print(time)

      
            event_location.append(name)
            event_location.append(venue)
            event_location.append(lat)
            event_location.append(lng)
            event_locations.append(event_location)
            event_location.append(event_id)
            event_location.append(date)

            if time is not None:

                time_object = datetime.strptime(time, '%H:%M:%S')
           

                time_string = datetime.strftime(time_object, "%I:%M %p")
                
                event_location.append(time_string)

            else:

                event_location.append(time)


            event_location.append(url)


    return event_locations


def generate_ids(event_list):


    length = len(event_list)
    ids = []

    for i in range(length):
        ids.append(i)

        print(ids)


def get_event_from_ids(event_id):


    request_string = (f'https://api.songkick.com/api/3.0/events/{event_id}.json?apikey={api_key}')
    
    event_to_save = requests.get(request_string)
    event_to_save = event_to_save.json()

    event = event_to_save['resultsPage']['results']['event']

    new_event = []

    event_id = event['id']
    name = event['displayName']
    venue = event['venue']['displayName']
    lat = event['venue']['lat']
    lng = event['venue']['lng']
    date = event['start']['date']
    time = event['start']['time']
    url = event['uri']


    new_event.append(event_id)
    new_event.append(name)
    new_event.append(venue)
    new_event.append(lat)
    new_event.append(lng)
    new_event.append(date)
    new_event.append(time)
    new_event.append(url)

    return new_event


def get_distances(event_locations, user_lat, user_lng):


    close_events = []

    user = (user_lat, user_lng)

    for event in event_locations:
        x = (event[2], event[3])
        event_distance = distance.distance(user, x).km
        if event_distance <= 5:
            event.append(event_distance)
            close_events.append(event)
  
    close_events_sorted = sorted(close_events, key = lambda x: x[8])
    
  
    return close_events_sorted



def get_db_events_by_user_id(user_id):

    user_events = UserEvent.query.filter_by(user_id=user_id).all()

    event_ids = []

    # loop through events user saved and append event ids to list to get event info
    for event in user_events:
        event_id = event.event_id
        event_ids.append(event_id)

    return event_ids


def get_db_events_by_event_id(event_ids):

    events = []
    future = []

    for event_id in event_ids:
        event = Event.query.filter_by(event_id=event_id).first()
        events.append(event)

    print("DATABASEEVENTS**", events)

    today = datetime.today()
    print("TODAY IS", today)
  
    for event in events:
        event_date = event.event_date
        if event_date.day >= today.day:
            future.append(event)

    print("FUTURE EVENTS:", future)

    for event in future:
        if event.event_time is not None:
            time_object = event.event_time
            time_string = datetime.strftime(time_object, "%I:%M %p")
            event.event_time = time_string

    for event in future:
        event_date = event.event_date
        date_string = date.strftime(event_date, "%b %d %Y")
        event.event_date = date_string
               

    return future


def make_time_object(event):

    time = event[6]
    if time is not None:

        time_object = datetime.strptime(time, '%H:%M:%S')

    else:
        time_object = None

    return time_object
      

def make_date_object(event):

    date = event[5]
    if date is not None:

        date_object = datetime.strptime(date, '%Y-%m-%d')

    return date_object

