from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, UserEvent

import requests

from helperfunctions import get_events_list_by_metro_area_and_date, get_metro_id_by_lat_lng, get_locations, get_metro_id_by_city, get_event_from_ids, get_distances, get_db_events_by_user_id, get_db_events_by_event_id, make_date_object, make_time_object

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
def get_landing_page():

    return render_template("landingpage2.html")





@app.route('/geoindex')
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

    if location == "" or location == False or location == None:
        return redirect('/geoindex')

    min_date = request.args.get("mind")

    if min_date == "" or min_date == False or min_date == None:
        return redirect('/geoindex')

    max_date = request.args.get("maxd")

    if max_date == "" or max_date == False or max_date == None:
        return redirect('/geoindex')

    
    print("*******", min_date)
    print("********", max_date)
    print("LOCATION", location)

    location = json.loads(location)

    user_lat, user_lng =  location["lat"], location["lng"]

    session["user_lat"] = user_lat
    session["user_lng"] = user_lng
    
    # pass city in to get metro ID
    metro_id = get_metro_id_by_lat_lng(user_lat, user_lng)
    print(metro_id)

    # pass in id and dates to get event list
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
    
    # pass events list in to get event locations
    event_locations = get_locations(event_list)
 
    # use geopy to filter out events that are far away (make this into helper function)
    close_events = get_distances(event_locations, user_lat, user_lng)
    print(close_events)


    return render_template("eventsmap.html", close_events=close_events, user_lat=user_lat, user_lng=user_lng)





@app.route('/citymap')
def get_city_map():
    """Display map showing events in the city entered by the user."""

    city = request.args.get("city")
    min_date = request.args.get("mind")
    max_date = request.args.get("maxd")
    print("*****", min_date)
    print("*****", max_date)
    # pass city in to get metro ID
    metro_id = get_metro_id_by_city(city)

    #pass metro id and dates in to get list of events
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
   
    # pass events list in to get event locations
    close_events = get_locations(event_list)
    print(close_events)

   
    return render_template("citysearcheventsmap.html", close_events=close_events)




@app.route('/getuserevents/<int:user_id>')
def events_index(user_id):
    """User event page to show events specific users have saved"""

    user = User.query.get(user_id)
    print(user)

    event_ids = get_db_events_by_user_id(user_id)
    print("HERE ARE IDSSSS", event_ids)

    events = get_db_events_by_event_id(event_ids)
    print("******", "HERE ARE SOME", events)


    return render_template("usersavedeventindex.html", user=user, events=events)




@app.route("/saveevents", methods=["GET", "POST"])
def save_events():


    if request.method == "POST":

        event_id = request.form.get('event_id')
        print("ID", event_id)

        new_event = get_event_from_ids(event_id)
        print("EVENT", new_event)

        time_object = make_time_object(new_event)
        print("TIME", time_object)
        date_object = make_date_object(new_event)
        print("DATE", date_object)

         # check is there is a user in session
        
        user_id = session["user_id"]
        print(user_id)

            # check if user has already saved this event
        if UserEvent.query.filter_by(event_id=event_id, user_id=user_id).all():
            flash('You already saved this event!')
            print('already saved')

            #check if event is in events database and if so, add just to user's events
        elif Event.query.filter_by(event_id=event_id).all():
            print('hiiiii')

            user_event = UserEvent(user_id=user_id, event_id=event_id)
            db.session.add(user_event)
            db.session.commit()
            print("committed to USER DB!")

            # if event is not in user's or master event database, create new event object
        else:
            print('putting in db')
            event = Event(event_id=new_event[0], event_name=new_event[1], event_venue=new_event[2],
             event_date=date_object, event_time=time_object, event_url=new_event[7], event_lat=new_event[3], event_lng=new_event[4])
            db.session.add(event)
            db.session.commit()

            user_event = UserEvent(user_id=user_id, event_id=event_id)
            db.session.add(user_event)
            db.session.commit()
            print("committed to USER DB!")

       

        # return render_template("userevents.html", saved_events=saved_events)
        # return redirect("eventsmap.html", saved_events=saved_events)
        return "Event Saved"
       



@app.route('/removeevents', methods=["GET", "POST"])
def remove_events():
    """Remove events from database."""

    if request.method == "POST":

        event_id = request.form.get('event_id')
        print(event_id)
        
        if "user_id" in session:
            user_id = session["user_id"]
            user = User.query.get(user_id)

            user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
            # delete event from user's data
            db.session.delete(user_event)
            db.session.commit()

            # to update events list, requery DB for user's events 
            event_ids = get_db_events_by_user_id(user_id)
            print(event_ids)

            events = get_db_events_by_event_id(event_ids)
            print(events)
    
            return render_template('usersavedeventindex.html', events=events, user=user)



@app.route("/showme")
def show_event():
    """Show directions from user's location to event."""


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