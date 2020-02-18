from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User

import requests

from API_Tests import get_events_list_by_metro_area_and_date, get_metro_id, get_locations

import json





app = Flask(__name__)


app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage for events list."""
    return render_template("homepage.html")


@app.route('/mapindex')
def mapindex():
    """Map events list homepage."""

    return render_template("maphomepage.html")


@app.route('/events')
def get_events_list():
    """Uses metro ID to get list of events around user."""
    city = request.args.get("city")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")

    metro_id = get_metro_id(city)


    event_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)


    # metro_id = str(metro_id)

    return render_template('events.html', event_list=event_list)



@app.route('/map')
def get_map():

    city = request.args.get("city")
    min_date = request.args.get("min_date")
    max_date = request.args.get("max_date")


    #pass city in to get metro ID
    metro_id = get_metro_id(city)
    print(metro_id)

    #pass metro id and dates in to get list of events
    events_list = get_events_list_by_metro_area_and_date(metro_id, min_date, max_date)
    print(events_list)

    # pass events list in to get event locations
    event_locations = get_locations(events_list)
    print(event_locations)
    # event_locations = json.dumps(event_locations)



    return render_template("basic_map.html", event_locations=event_locations)



    


# @app.route("/register", methods=["GET"])
# def register_form():

#     return render_template('register_form.html')


# @app.route("/register", methods=["POST"])
# def register_process():

#     email = request.form.get('email')
#     password = request.form.get('password')

#     if User.query.filter_by(email=email).all():
#         return redirect("/")

#     else:
#         # add to database
#         user = User(email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
     

#     return redirect("/")



# @app.route("/login", methods=["GET"])
# def login_form():

#     return render_template('login_form.html')



# @app.route("/login", methods=["POST"])
# def login_process():

#     email = request.form.get('email')
#     password = request.form.get('password')

#     if User.query.filter(email == email, password == password).all():
        
        
#         # query user_id
#         user = User.query.filter(email ==email, password ==password).first()

#         session['current_user'] = user.user_id
#         ## fix sessions- left off here, try to find session notes for reference
        
#         flash(f'Logged in! Hi User # {user.user_id}')
        
#         return redirect(f"/{user.user_id}")

#     else:
#         flash("Invalid Email and Password")
        
#         return redirect("/")  

#     return redirect("/")


# @app.route("/logout")
# def logout_process():
#     session.clear()
#     flash("You've been logged out!")

#     return redirect("/")

# # <form action='/{{ user.user_id }}' method='post'>
# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/users/<int:user_id>")
# def user_details(user_id):

#     user = User.query.get(user_id)
#     user_id = user.user_id
#     user_zip = user.zipcode
#     user_age = user.age

#     user_ratings = Rating.query.filter(user_id == user_id).all()


#     return render_template('user_details.html', user_id=user_id, user_zip=user_zip, user_age=user_age, user_ratings=user_ratings)



# @app.route("/movies")
# def movie_list():
#     """Show list of users."""

#     movies = Movie.query.all()
#     return render_template("movie_list.html", movies=movies)


# @app.route("/movies/<int:movie_id>")
# def movie_details(movie_id):

#     movie = Movie.query.get(movie_id)
#     movie_id = movie.movie_id
#     user_zip = user.zipcode
#     user_age = user.age

#     user_ratings = Rating.query.filter(user_id == user_id).all()


#     return render_template('user_details.html', user_id=user_id, user_zip=user_zip, user_age=user_age, user_ratings=user_ratings)


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