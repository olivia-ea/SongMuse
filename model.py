"""Models and databases"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MODELS GO HERE

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password = db.Column(db.String(64), nullable=True)
    # token if needed

    def __repr__(self):
        return f'<User user_id={self.user_id}>'

class Song(db.model):
    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(64), nullable=True)
    artist_name = db.Column(db.String(64), nullable=True)
    # how to take into account multiple artist names

    def __repr__(self):
        return f'<Song song_id={self.song_id} song_name={self.song_name} artist_name={self.artist_name}>'

class Playlist(db.Model):
    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return f'<User user_id={self.user_id}>'


# class Artist(db.model):
#     pass

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