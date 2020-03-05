from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, UserEvent

import requests

from API_Tests import get_events_list_by_metro_area_and_date, get_metro_id_by_lat_lng, get_locations, get_metro_id_by_city, get_event_from_ids

import json

from datetime import datetime

import os

import hashlib

from geopy import distance



api_key = os.environ['SK_KEY']




app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined




@app.route('/')
def geolocationindex():
    """Geolocation search homepage"""

    return render_template("homepage.html")



@app.route('/cityindex')
def cityindex():
    """City search homepage."""

    return render_template("citysearchpage.html")



@app.route('/map')
def get_map():
    """Display map showing events based on geolocation of user."""

    location = request.args.get("location")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")

    location = json.loads(location)

    lat = location["lat"]
    lng = location["lng"]

    session["user_lng"] = lng
    session["user_lat"] = lat

    print(session.get("user_lat"))


    # if user in session:
    #     user_id = session["user_id"]


    
    # pass city in to get metro ID
    metro_id = get_metro_id_by_lat_lng(lat, lng)
    print(metro_id)

    # pass in id and dates to get event list
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
    
    # pass events list in to get event locations
    event_locations = get_locations(event_list)
 
    # use geopy to filter out events that are far away (make this into helper function)
    close_events = []

    for event in event_locations:
        user = (lat, lng)
        x = (event[2], event[3])
        event_distance = distance.distance(user, x).km
        if event_distance <= 5:
            close_events.append(event)


    return render_template("eventsmap.html", close_events=close_events, lat=lat, lng=lng)



@app.route('/citymap')
def get_city_map():
    """Display map showing events in the city entered by the user."""


    city = request.args.get("city")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")

    # pass city in to get metro ID
    metro_id = get_metro_id_by_city(city)

    #pass metro id and dates in to get list of events
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
   
    # pass events list in to get event locations
    event_locations = get_locations(event_list)

   
    return render_template("citysearcheventsmap.html", events=events)



@app.route('/getuserevents/<int:user_id>')
def events_index(user_id):
    """User event page to show events specific users have saved"""

    user = User.query.get(user_id)

    user_events = UserEvent.query.filter_by(user_id=user_id).all()

    event_ids = []

    # loop through events user saved and append event ids to list to get event info
    for event in user_events:
        event_id = event.event_id
        event_ids.append(event_id)

    events = []

    for event_id in event_ids:
        event = Event.query.filter_by(event_id=event_id).first()
        events.append(event)

    # check if dates are in the past- if so, do not add to list
    future_events = []

    for event in events:
        Event.query.filter(event.event_date < datetime.now()).all()
        future_events.append(event)

    # change event objects into dictionary
    events_dict = {}

    for event in future_events:

        events_dict['event'] = {'event_id': event.event_id,
        'name': event.event_name,
        'venue': event.event_venue,
        'date': event.event_date,
        'time': event.event_time,
        'url': event.event_url,
        'lat': event.event_lat,
        'lng': event.event_lng }


    return render_template("usersavedeventindex.html", user=user, events=events, events_dict=events_dict)


@app.route("/saveeventsfromwindow")
def save_from_window():


    event_id_window =request.form.get('windowbutton')
    print("IDIDIDID*******", event_id_window, "*******************")

    return "HI"



@app.route("/saveevents", methods=["GET", "POST"])
def save_events():


    if request.method == "POST":

        event_id = request.form.get('event_id')

        event = get_event_from_ids(event_id)

        #create new event from json to put into database
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


        if time is not None:

            time_object = datetime.strptime(time, '%H:%M:%S')
            print("***", time, "*******")

        else:
            time_object = None

        if date is not None:

            date_object = datetime.strptime(date, '%Y-%m-%d')
        
        # check is there is a user in session
        if "user_id" in session:
            user_id = session["user_id"]


            # check if user has already saved this event
            if UserEvent.query.filter_by(event_id=event_id, user_id=user_id).all():
                flash(f'You have saved this event!')


            #check if event is in events database and if so, add just to user's events
            if Event.query.filter_by(event_id=event_id).all():

                user_event = UserEvent(user_id=user_id, event_id=event_id)
                db.session.add(user_event)
                db.session.commit()


            # if event is not in user's or master event database
            else:
                event = Event(event_id=new_event[0], event_name=new_event[1], event_venue=new_event[2],
                 event_date=date_object, event_time=time_object, event_url=new_event[7], event_lat=new_event[3], event_lng=new_event[4])
                db.session.add(event)
                db.session.commit()

            
        else: 
            flash(f'Please log in to save events!')


        # return render_template("userevents.html", saved_events=saved_events)
        # return redirect("eventsmap.html", saved_events=saved_events)
        return "Event Saved"
       


@app.route('/removeevents', methods=["GET", "POST"])
def remove_events():
    """Remove events from database."""

    if request.method == "POST":

        event_id = request.form.get('event_id')
        
        if "user_id" in session:
            user_id = session["user_id"]
            user = User.query.get(user_id)

            user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
            # delete event from user's data
            db.session.delete(user_event)
            db.session.commit()

            # to update events list, requery DB for user's events 
            user_events = UserEvent.query.filter_by(user_id=user_id).all()

            event_ids = []

            # loop through events user saved and append event ids to list to search later
            for event in user_events:
                event_id = event.event_id
                event_ids.append(event_id)

            events = []

            for event_id in event_ids:
                event = Event.query.filter_by(event_id=event_id).first()
                events.append(event)


            return render_template('usersavedeventindex.html', events=events, user=user)



@app.route("/showme")
def show_event():


    event_id = request.args.get('event')
    print(event_id)

    if "user_lat" in session:
        user_lat = session["user_lat"]
   
    if "user_lng" in session:
        user_lng = session["user_lng"]


    event = Event.query.filter_by(event_id=event_id).first()

    event_lat = event.event_lat
    event_lng = event.event_lng



    return render_template('individualeventpage.html', user_lat=user_lat, user_lng=user_lng, event_lat=event_lat, event_lng=event_lng )




# REGISTRATION AND USER LOGIN  *******************************************



@app.route("/register")
def register_form():
    """Registration homepage"""


    return render_template('register.html')



@app.route("/register", methods=["POST"])
def register_process():
    """Sends info to database"""

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).all():
        flash(f'Already registered! Please login.')
        return redirect("/")

    else:
        # add to database
        hashed_pw = hashlib.md5(password.encode()).hexdigest()

        user = User(email=email, password=hashed_pw, name=name)
        db.session.add(user)
        db.session.commit()
     

    return redirect("/")



@app.route("/login", methods=["GET"])
def login_form():
    """Login form for users"""

    return render_template('login.html')



@app.route("/login", methods=["POST"])
def login_process():
    """Processing user login"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != hashlib.md5(password.encode()).hexdigest():
        flash("Incorrect password")

        return redirect("/login")

    else:

        session["user_id"] = user.user_id

        flash("Logged in!")

        return redirect(f"/getuserevents/{user.user_id}")



@app.route("/logout")
def logout_process():
    """User logout, clears session."""

    if "user_id" in session:
        del session["user_id"]
        flash("Logged Out.")
        return redirect("/")

    else:
        flash(f'You are not logged in!')
        return redirect("/")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')