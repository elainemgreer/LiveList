import json
import requests
from pprint import pprint
import os


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


            event_location.append(name)
            event_location.append(venue)
            event_location.append(lat)
            event_location.append(lng)
            event_locations.append(event_location)
            event_location.append(event_id)
            event_location.append(date)
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

    event_to_save = event_to_save['resultsPage']['results']['event']

    return event_to_save





