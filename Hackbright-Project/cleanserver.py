from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User

import requests

from API_Tests import get_events_list_by_metro_area_and_date, get_metro_id, get_locations

import json



app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined





@app.route('/')
def mapindex():
    """Map events list homepage."""

    return render_template("cleanhomepage.html")







@app.route('/map')
def get_map():
    """Display map showing events in the city entered by the user."""

    city = request.args.get("city")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")


    #pass city in to get metro ID
    metro_id = get_metro_id(city)
    print(metro_id)

    #pass metro id and dates in to get list of events
    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
    print(event_list)

    # pass events list in to get event locations
    event_locations = get_locations(event_list)
    print(event_locations)
    # event_locations = json.dumps(event_locations)



    return render_template("cleaneventsmap.html", event_locations=event_locations, event_list=event_list)






# REGISTRATION AND USER LOGIN






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








@app.route('/userlocation')
def get_user_location():


    user_location = request.get_json()
    print("1st", user_location)
    json = jsonify(user_location)

    # min_date = request.form.get("min_date")
    # print(min_date)
    # max_date = request.form.get("max_date")
    # print(max_date)
   
    user_location =  jsonify(user_location)
    print("************", user_location)

    # latitude = user_location['location']['lat']
    # print(latitude)
    # longitude = user_location['location']['lng']
    # print(longitude)
 

    # metro_id = get_metro_id(latitude, longitude)
    # print(metro_id)

    return json





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