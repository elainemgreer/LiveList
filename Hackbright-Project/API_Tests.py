import json
import requests
from pprint import pprint
import os


api_key= os.environ['SK_KEY']

def get_metro_id(latitude, longitude):
    """Gets metro ID of user to use to find events"""


    request_string = (f'https://api.songkick.com/api/3.0/search/locations.json?location=geo:{latitude},{longitude}&apikey={api_key}')

    metro_id_results = requests.get(request_string)

    json = metro_id_results.json()

    # print(json)

    # pp_json = pprint(json)

    # print(pp_json)

    location = json['resultsPage']['results']['location']
    city_dict = location[0]
    metro = city_dict['metroArea']
    metro_id = metro['id']

    return metro_id


metro_id = get_metro_id(37.788920, -122.411535)






def get_events_list_by_metro_area_and_date(metro_id, min_date, max_date):
    """Uses metro ID to get list of events around user."""

    metro_id = str(metro_id)

    

    payload = {'apikey': api_key,
            'metro_area_id': metro_id,
            'min_date': min_date,
            'max_date': max_date}


    events_json = requests.get('https://api.songkick.com/api/3.0/events.json',
            params=payload)

    # event_results = requests.get(request_string)

    events_json = events_json.json()
    # return events_json

    # num_events = events_json['resultsPage']['totalEntries'] 
    # print("*************" num_events "******************")


    events_list = events_json['resultsPage']['results']['event']



    # for event in events_list:

    #     events_dict['name'] = (event['displayName'])
    #     events_dict['venue'] = (event['venue']['displayName'])
    #     events_dict['date'] = (event['start']['date'])
    #     events_dict['time'] = (event['start']['time'])

    
    return events_list


# get_events_list_by_metro_area_and_date('26330', '2020-02-13', '2020-02-17')



def find_num_events(events_json):

    num_events = events_json['resultsPage']['totalEntries']

    return num_events


# number_events = find_num_events(events_json)


def get_all_pages(num_events):


    if num_events > 50:
        num_pages = num_events / 50

    rounded = round(num_pages)
    num_pages = int(rounded)
        
    return num_pages




# number_pages = get_all_pages(number_events)
# print(number_pages)




def loop_over_pages(events_json):

    number_events = find_num_events(events_json)
    print(number_events)

    number_pages = get_all_pages(number_events)
    print(number_pages)

    page_number = 1

    payload = {'apikey': api_key,
            'metro_area_id': '26630',
            'min_date': '2020-02-13',
            'max_date': '2020-02-16',
            'page': str(page_number) }

    
    pages = []

    while page_number < number_pages:
        page = requests.get('https://api.songkick.com/api/3.0/events.json',
            params=payload)
        json_page = page.json()
        print(json_page)
        # pages.append(page)
        page_number = page_number + 1


    # print(pages)
    # return pages



# result = loop_over_pages(events_json)
# print(result)




