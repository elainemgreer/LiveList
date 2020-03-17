# LiveList
> LiveList is a full-stack web application to find and store musical events. It allows users to search either by geolocation or by city and see events in both map and list view. Users can also store their favorite events into a personalized events list; from this list they can see event details and get directions to events of their choice. 

This project was made at Hackbright Academy in San Francisco over four weeks in February-March 2020.

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/landingpage.png "Homepage")

# Contents

- Technologies
- Features
- Installation
- About the Engineer

## Technologies

Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, AJAX, PostgreSQL, SQLAlchemy, Bootstrap

APIs: Google Maps JavaScript, Google Maps Directions, Songkick API

## Features:

- Registration, Login, Logout
- Geolocation Search
- City Search with Autocomplete
- Event Map and List
- Like Heart Button
- GeoPy Sorted Events List 
- Ability to Manage and Remove Events
- Directions
- Hashed Passwords

### Geolocation Search:

![alt text](https://github.com/elainemgreer/Hackbright-Project/blob/master/Hackbright-Project/static/images/searchpage.png "search page")

### Search Results (Map + List View):

![](websitegif.gif)

### Saved Events Page:

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

## About the Engineer

Elaine Greer is a native Texan, former educator, and musician with a degree in philosophy. Before entering into the world of software engineering, Elaine worked at a Beijing based online education start-up company in teacher management and curriculum design. Before that, she taught in the classroom for several years. Elaine has experience working in varied cultural environments and is highly adaptable, as she has lived and worked in both France and China. Coming from a creative background, Elaine is resourceful in her approach to solving problems and is excited about working in a field that presents intellectual challenges and endless opportunities for continued learning and growth. Most recently, Elaine attended the 12-week immersive full-stack 
software engineering program at Hackbright Academy in San Francisco.

Elaine Greer – [LinkedIn](https://www.linkedin.com/in/elainemgreer/) – elainemichellegreer@gmail.com

[Github](https://github.com/elainemgreer/)

