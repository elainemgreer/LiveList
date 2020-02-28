
"""Models and database functions for events project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class User(db.Model):
    """User of events website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    # default_location = db.Column(db.String(64), nullable=True)
   

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"



class Event(db.Model):
    """Musical Event"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_name = db.Column(db.String(100), nullable=True)
    event_venue = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.DateTime, nullable=True)
    event_time = db.Column(db.DateTime, nullable=True)
    event_url = db.Column(db.String(200), nullable=True)
    event_lat = db.Column(db.Float, nullable= False)
    event_lng = db.Column(db.Float, nullable=False)



    def __repr__(self):
        """Provide representation of genre when printed."""

        return f"<Event event_id={self.event_id} name={self.event_name}>"


class UserEvent(db.Model):

    __tablename__ = "user_events"

    user_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    def __repr__(self):

        return f"<UserEvent user_id={self.user_id} event_id={self.event_id}>"






def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
 
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
