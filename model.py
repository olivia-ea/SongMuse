"""Models and databases"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    auth_token = db.Column(db.String(500), nullable=False)
    refresh_token = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id}>'

class Activity(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('activities')) 

    def __repr__(self):
        return f'<Activity activity_id={self.activity_id} activity_name={self.activity_name}>'


class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), nullable=False)
    playlist_uri = db.Column(db.String(100), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('playlists')) 
    activity = db.relationship('Activity', backref=db.backref('playlists')) 

    def __repr__(self):
        return f'<Playlist playlist_id={self.playlist_id} playlist_name={self.playlist_name}>'

class Song(db.Model):
    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    song_uri = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Song song_name={self.song_name} artist_name={self.artist_name} song_uri={self.song_uri}>'

class Playlist_Song(db.Model):
    __tablename__ = "playlists_songs"

    playlist_song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)

    playlist = db.relationship('Playlist', backref=db.backref('playlists_songs')) 
    song = db.relationship('Song', backref=db.backref('playlists_songs')) 

    def __repr__(self):
        return f'<Playlist_Song playlist_song_id={self.playlist_song_id}>'

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
    print('Connected to DB.')

