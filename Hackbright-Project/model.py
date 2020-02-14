
"""Models and database functions for events project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class User(db.Model):
    """User of events website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
   

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"



class Genre(db.Model):
    """Music genre"""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=True)


    def __repr__(self):
        """Provide representation of genre when printed."""

        return f"<Genre genre_id={self.genre_id} name={self.genre_name}>"


class UserGenre(db.Model):

    __tablename__ = "user_genres"

    user_genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

    def __repr__(self):

        return f"<UserGenre user_id={self.user_id} genre_id={self.genre_id}>"






def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
 
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
