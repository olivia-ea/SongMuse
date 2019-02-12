"""Models and databases"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MODELS GO HERE

class User(db.Model):
    pass

class Playlist(db.Model):
    pass

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")