"""Models and databases"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

class Activity(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    activity_name = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', backref=db.backref('activities')) 

    #secondary='users_activities',

    def __repr__(self):
        return f'<Activity activity_id={self.activity_id} activity_name={self.activity_name}>'

# class User_Activity(db.Model):
#     __tablename__ = 'users_activities'

#     user_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
#     activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), index=True)

#     user = db.relationship('User', seconday='activities', backref=db.backref('users_activities'))

#     def __repr__(self):
#         return f'<User_Activity user_activity_id={self.user_activity_id}>'

class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    # activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), index=True)
    playlist_name = db.Column(db.String(50), nullable=True)

    # user = db.relationship('User', backref=db.backref('playlists')) 
    # activity = db.relationship('Activity', backref=db.backref('playlists')) 

    def __repr__(self):
        return f'<Playlist playlist_id={self.playlist_id} playlist_name={self.playlist_name}>'

class Song(db.Model):
    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(50), nullable=True)
    artist_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Song song_id={self.song_id} song_name={self.song_name} artist_name={self.artist_name}>'

class Playlist_Song(db.Model):
    __tablename__ = "playlists_songs"

    playlist_song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)    
    # # playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), index=True)
    # # song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), index=True)

    # playlist = db.relationship('Playlist', backref=db.backref('playlists_songs')) 
    # song = db.relationship('Song', backref=db.backref('playlists_songs')) 


    def __repr__(self):
        return f'<Playlist_Song playlist_song_id={self.playlist_song_id}>'


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all( )
    print('Connected to DB.')