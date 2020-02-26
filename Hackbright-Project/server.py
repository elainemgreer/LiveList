from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, UserEvent

import requests

from API_Tests import get_events_list_by_metro_area_and_date, get_metro_id_by_lat_lng, get_locations, get_metro_id_by_city, get_event_from_ids

import json

from datetime import datetime

import os



api_key = os.environ['SK_KEY']



app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


### homepage


@app.route('/')
def mapindex():
    """Map events list homepage."""

    return render_template("homepage.html")





## events by lat/lng
@app.route('/map')
def get_map():
    """Display map showing events in the city entered by the user."""


    location = request.args.get("location")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")
    print("*" * 100)
    print(location, min_date, max_date)
    print("*" * 100)

    location = json.loads(location)
    lat = location["lat"]
    lng = location["lng"]


    
    # pass city in to get metro ID
    metro_id = get_metro_id_by_lat_lng(lat, lng)
    print(metro_id)

    # d = datetime.datetime.today()
    # print(d)
    # print(d.year, d.month, d.day)
    # print("************************************")
    # print("datetime day", d.day)

    # date_list = max_date.split("-")
    # day = int(date_list[2])
    # print(day)
    # print(d.day)

    # now = datetime.datetime.now()
    # print("now", now)

    # if day <= d.day - 1:
    #     flash(f'This date has already passed. Please choose a valid date.')
    #     return redirect("/")

    # else:

    #pass metro id and dates in to get list of events
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)

    print("**************", event_list, "*******************")
    
    # pass events list in to get event locations
    event_locations = get_locations(event_list)
 
    # event_locations = json.dumps(event_locations)
    close_events = []

    for event in event_locations:
        if lat - event[2] <= .2:
            close_events.append(event)

    # length = len(close_events)
    # ids = []

    # for i in range(length):
    #     ids.append(i)

    #     print(ids)

    print(close_events)

    # id = 0

    # for event_object in close_events:
    #     event_object.append(id)
    #     id += 1

    # print(close_events)


    

    return render_template("eventsmap.html", close_events=close_events)





@app.route("/saveevents", methods=["GET", "POST"])
def get_saved_events():

    if request.method == "POST":

        events_to_save = request.form.getlist("events")
        print(events_to_save)

        event_info = request.form.getlist("eventinfo")

        saved_events = []

        for event_id in events_to_save:
            event = get_event_from_ids(event_id)
            print(event)


            new_event = []

            event_id = event['id']
            name = event['displayName']
            venue = event['venue']['displayName']
            lat = event['venue']['lat']
            lng = event['venue']['lng']
            date = event['start']['date']
            time = event['start']['time']

            new_event.append(event_id)
            new_event.append(name)
            new_event.append(venue)
            new_event.append(lat)
            new_event.append(lng)
            new_event.append(date)
            new_event.append(time)
           

            saved_events.append(new_event)


            if 'current_user' in session:
                user_id = session['current_user']
                
            else: 
                flash(f'Please log in to save events!')

            if time is not None:

                time_object = datetime.strptime(time, '%H:%M:%S')
                print("***", time, "*******")

            if date is not None:

                date_object = datetime.strptime(date, '%Y-%m-%d')
                print(date_object)
            ## change date and time into datetime objects instead of strings!!

            if Event.query.filter_by(event_id=event_id).all():
                flash(f'Event already saved')

            else:

                event = Event(event_id=new_event[0], event_name=new_event[1], event_venue=new_event[2], event_date=date_object, event_time=time_object)
                db.session.add(event)
                db.session.commit()

                user_event = UserEvent(user_id=user_id, event_id=event_id)
                db.session.add(user_event)
                db.session.commit()


        print(saved_events)

        return render_template("userevents.html", saved_events=saved_events)
   

        





        # events = []

        # for event in event_info:
        #     event = [event]
        #     events.append(event)

        # print(events)

      

        # saved_events = []

        # for event_id in events_to_save:
        #     for event in event_info:
        #         if event[4] == event_id:
        #             saved_events.append(event)

        # print(saved_events)


  




# @app.route("/savedeventsmap")
# def show_saved_events():




        








## route for displaying map by city search
@app.route('/citymap')
def get_city_map():
    """Display map showing events in the city entered by the user."""


    city = request.args.get("city")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")
    print("*" * 100)
    print(city, min_date, max_date)
    print("*" * 100)



    # pass city in to get metro ID
    metro_id = get_metro_id_by_city(city)

    print(metro_id)

    #pass metro id and dates in to get list of events
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
    print(event_list)

    # pass events list in to get event locations
    close_events = get_locations(event_list)
    
    # event_locations = json.dumps(event_locations)


    return render_template("cleaneventsmap.html", close_events=close_events, event_list=event_list)







# REGISTRATION AND USER LOGIN  *******************************************



@app.route("/register")
def register_form():


    return render_template('register.html')




@app.route("/register", methods=["POST"])
def register_process():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).all():
        flash(f'Already registered! Please login.')
        return redirect("/")

    else:
        # add to database
        user = User(email=email, password=password, name=name)
        db.session.add(user)
        db.session.commit()
     

    return redirect("/")




@app.route("/login", methods=["GET"])
def login_form():

    return render_template('login.html')




@app.route("/login", methods=["POST"])
def login_process():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in!")

    return redirect("/")





@app.route("/logout")
def logout_process():

    if user in session:
        del session["user_id"]
        flash("Logged Out.")
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