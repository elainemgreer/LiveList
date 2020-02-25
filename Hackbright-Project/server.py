from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User

import requests

from API_Tests import get_events_list_by_metro_area_and_date, get_metro_id_by_lat_lng, get_locations, get_metro_id_by_city

import json

import datetime



app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


### homepage


@app.route('/')
def mapindex():
    """Map events list homepage."""

    return render_template("homepage2.html")





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
    
    # pass events list in to get event locations
    event_locations = get_locations(event_list)
 
    # event_locations = json.dumps(event_locations)
    close_events = []

    for event in event_locations:
        if lat - event[2] <= .3:
            close_events.append(event)

    # length = len(close_events)
    # ids = []

    # for i in range(length):
    #     ids.append(i)

    #     print(ids)

    print(close_events)

    id = 0

    for event_object in close_events:
        event_object.append(id)
        id += 1

    print(close_events)


    

    return render_template("eventsmap.html", close_events=close_events)





@app.route("/saveevents", methods=["GET", "POST"])
def get_saved_events():

    if request.method == "POST":

        events_to_save = request.form.getlist("events")
        print(events_to_save)




    return redirect("/")


@app.route("/savedeventsmap")
def show_saved_events():

    


        








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

    if User.query.filter(email == email, password == password).all():
        
        
        # query user_id
        user = User.query.filter(email ==email, password ==password).first()

        session['current_user'] = user.user_id
        ## fix sessions- left off here, try to find session notes for reference
        
        flash(f'Logged in! Hi {user.name}')
        
        return redirect("/")

    else:
        flash("Invalid Email and Password")
        
        return redirect("/")  

    return redirect("/")




@app.route("/logout")
def logout_process():
    session.clear()
    flash("You've been logged out!")

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