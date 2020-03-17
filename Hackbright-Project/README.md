# LiveList
> LiveList is a full-stack web application to find and store musical events. It allows users to search either by geolocation or by city and see events in both map and list view. Users can also store their favorite events into a personalized events list; from this list they can see event details and get directions to events of their choice. 

This project was made at Hackbright Academy in San Francisco over four weeks in February-March 2020.

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/landingpage.png "Homepage")


## Technologies


Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, AJAX, PostgreSQL, SQLAlchemy, Bootstrap, Geopy, Hashlib

APIs: Google Maps JavaScript, Google Maps Directions, Songkick API


## Overview

###Features:
- Registration, Login, Logout
- Geolocation Search
- City Search with Autocomplete
- Event Map and List
- Like Heart Button
- GeoPy Sorted Events List 
- Ability to Manage and Remove Events
- Directions
- Hashed Passwords


Geolocation Search:

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/searchpage.png "search page")

Search Results (Map + List View):

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/searchresultspage.png "search results")

Saved Events Page:

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/savedeventspage.png "saved events")



## <a name="installation"></a>Installation

### Prerequisites

You must have the following installed to run LiveList:

- PostgreSQL
- Python 3.x
- API key for Google Maps JavaScript API, Google Maps Places API, Songkick API

### Run LiveList on your local computer

Clone or fork repository:
```
$ git clone https://github.com/elainemgreer/LiveList
```
Create and activate a virtual environment inside your livelist directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Add your Songkick API key into the header script in server.py. Add Google Maps API key to scripts in templates: homepage.html, citysearchpage.html, citysearcheventsmap.html, eventsmap.html, individualeventpage.html.
<br><br>

Create database 'users':
```
$ createdb users
```
Run model.py interactively in the terminal, and create database tables:
```
$ python3 -i model.py
>>> db.create_all()
>>> quit()
```
Run the app from the command line.

```
$ python server.py

```


Elaine Greer – [LinkedIn](https://www.linkedin.com/in/elainemgreer/) – elainemichellegreer@gmail.com


[https://github.com/elainemgreer/](https://github.com/elainemgreer/)

