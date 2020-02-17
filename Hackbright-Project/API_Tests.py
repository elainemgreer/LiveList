import json
import requests
from pprint import pprint
import os


api_key = os.environ['SK_KEY']




# def get_metro_id(latitude, longitude):
#     """Gets metro ID of user to use to find events"""


#     request_string = (f'https://api.songkick.com/api/3.0/search/locations.json?location=geo:{latitude},{longitude}&apikey={api_key}')

#     metro_id_results = requests.get(request_string)

#     json = metro_id_results.json()

#     # print(json)

#     # pp_json = pprint(json)

#     # print(pp_json)

#     location = json['resultsPage']['results']['location']
#     city_dict = location[0]
#     metro = city_dict['metroArea']
#     metro_id = metro['id']

#     return metro_id


# metro_id = get_metro_id(37.788920, -122.411535)

def get_metro_id(city):
    """Gets metro ID of user to use to find events"""


    request_string = (f'https://api.songkick.com/api/3.0/search/locations.json?query={city}&apikey={api_key}')

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



events_list = get_events_list_by_metro_area_and_date('26330', '2020-02-17', '2020-02-17')
# print(event_list)




### FINISH THIS FUNCTION to make a dictionary of venues with lat/long coordinates 
def get_locations(event_list):

    # venue_names = []
    # lat_lng_tuples = []


    # for event in event_list:

    #     venue = event['venue']['displayName']
    #     venue_names.append(venue)

    #     lat = event['venue']['lat']
    #     lng = event['venue']['lng']
    #     lat_lng_tuples.append(tuple([lat,lng]))

    #     # print(venue, lat, lng)
    #     print(venue_names)
    #     print(lat_lng_tuples)

    # venue_dict = {}


    # for venue in venue_names:
    #     if venue not in venue_dict.keys():
    #         venue_dict[venue] = venue_dict.get(venue) 

    # print(venue_dict)

    # length = len(venue_names)

    # for i in range(len(lat_lng_tuples)):
    #     venue_dict[venue] = i
    #     i = i + 1

    event_locations = []

    for event in events_list:

        event_location = []

        venue = event['venue']['displayName']
        lat = event['venue']['lat']
        lng = event['venue']['lng']
        event_location.append(venue)
        event_location.append(lat)
        event_location.append(lng)
        event_locations.append(event_location)

        # for event in events_list:

        #     # venue = event['venue']['displayName']
        #     # lat = event['venue']['lat']
        #     # lng = event['venue']['lng']
        #     # event_location.append(venue)
        #     # event_location.append(lat)
        #     # event_location.append(lng)
       
        #     events.append(event_location)

    return event_locations


get_locations(events_list)










# def find_num_events(events_json):

#     num_events = events_json['resultsPage']['totalEntries']

#     return num_events


# # number_events = find_num_events(events_json)


# def get_all_pages(num_events):


#     if num_events > 50:
#         num_pages = num_events / 50

#     rounded = round(num_pages)
#     num_pages = int(rounded)
        
#     return num_pages




# number_pages = get_all_pages(number_events)
# print(number_pages)




# def loop_over_pages():



#     page_number = 1

#     payload = {'apikey': api_key,
#         'metro_area_id': '26630',
#         'min_date': '2020-02-13',
#         'max_date': '2020-02-16',
#         'page': page_number }


#     events_json = requests.get('https://api.songkick.com/api/3.0/events.json',
#             params=payload)

#     events_json.json()

#     print(events_json)


#     number_events = find_num_events(events_json)
#     print(number_events)

#     number_pages = get_all_pages(number_events)
#     print(number_pages)

    
#     pages = []

#     while page_number < number_pages:
#         page = requests.get('https://api.songkick.com/api/3.0/events.json',
#             params=payload)
#         json_page = page.json()
#         print(json_page)
#         # pages.append(page)
#         payload['page'] = str(page_number + 1)


#     print(pages)
#     return pages



# result = loop_over_pages()
# print(result)




