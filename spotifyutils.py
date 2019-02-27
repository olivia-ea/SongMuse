import json
import requests
import sys
import base64
from settings import *
from views import *
from flask import request, flash, session
from model import db, connect_to_db, User, Playlist, Song, Activity, Playlist_Song

def generate_auth_url():
    """ Returns user authorization url. 
    Used in '/spotify-login' route. """

    spotify_auth_url = (SPOTIFY_AUTH_URL + '?client_id=' + auth_query_param['client_id'] +
                        '&response_type=' + auth_query_param['response_type'] + 
                        '&redirect_uri=' + auth_query_param['redirect_uri'] + 
                        '&scope=' + auth_query_param['scope'])

    return spotify_auth_url

def get_access_token():
    """ Returns authorization token from Spotify. 
    Used in '/spotify-callback' route. """

    auth_code = request.args['code']

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_code),
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    base64encoded = base64.b64encode(("{}:{}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    return post_request.json()

def auth_header(token):
    """ Returns Spotify's authorization header. """

    return {"Authorization" : f"Bearer {token}"}

def get_user_id(auth_header):
    """ Return user's spotify ID.  """ 

    request = "{}/{}".format(SPOTIFY_API_URL, 'me')
    user_info_data = requests.get(request, headers=auth_header).json()
    user_id = user_info_data['id']

    return user_id

def create_playlist(auth_header, spotify_user_id, playlist_name, activity_id):
    """ Creates playlist locally and on user's Spotify account. """

    payload = { 
        'name' : playlist_name
        # 'description': description
        }

    USER_PLAYLIST_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, 'users', spotify_user_id, 'playlists')
    playlist_data = requests.post(USER_PLAYLIST_ENDPOINT, data=json.dumps(payload), headers=auth_header).json()
    playlist_uri = playlist_data['uri']
    user_id = session.get('logged_user')['username']

    new_playlist = Playlist(playlist_name = playlist_name,
                                user_id = user_id,
                                playlist_uri = playlist_uri, 
                                activity_id = activity_id)
    db.session.add(new_playlist)
    db.session.commit()

    playlist_id = new_playlist.playlist_id
    
    return playlist_id

def search_playlists(activity_query):
    """ Searches Spotify for playlists based on user's activity-related query.
    Returns list of playlist id numbers from API response. """ 

    PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q="+ activity_query +"&type=playlist&limit=5&offset=5")
    token = session.get('access_token')
    response = requests.get(PLAYLIST_ENDPOINT, headers=auth_header(token)).json()

    spotify_playlists_ids = []
    for i in range(0, 5):
        playlist_id = (response['playlists']['items'][i]['id'])
        spotify_playlists_ids.append(playlist_id)

    return spotify_playlists_ids

def search_playlists_tracks(spotify_playlists_ids, playlist_id):
    """ Finds the tracks based off the id number. 
        Adds songs to local songs table. 
        Add songs and playlist id to local playlists_songs table. """

    playlist_1, playlist_2, playlist_3, playlist_4, playlist_5 = spotify_playlists_ids

    for playlist in spotify_playlists_ids:
        TRACK_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, "playlists", playlist, "tracks?market=US&limit=5&offset=5")
        token = session.get('access_token')
        response = requests.get(TRACK_ENDPOINT, headers=auth_header(token)).json()
        for i in range(0, 5):
            track_name = (response['items'][i]['track']['name'])
            track_artist = (response['items'][i]['track']['artists'][0]['name'])
            track_uri = (response['items'][i]['track']['uri'])
            new_song = Song(song_name=track_name, artist_name=track_artist, song_uri=track_uri)
            db.session.add(new_song)
            db.session.commit()
            new_playlist_song = Playlist_Song(playlist_id=playlist_id, song_id=new_song.song_id)
            db.session.add(new_playlist_song)
            db.session.commit()

    return ('Added to DB.')

def seed_spotify_playlist(auth_header, playlist_id):
    """ Queries to playlists_songs table to add songs from given playlist_uri 
    to user's spotify account. """
    token = session.get('access_token')

    playlist = Playlist.query.filter_by(playlist_id=playlist_id).one()

    queries = Playlist_Song.query.filter_by(playlist_id=playlist_id).all()

    for query in queries:
        PLAYLIST_TRACK_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, 'playlists', playlist.playlist_uri, 'tracks?uri=' + query.song.song_uri)
        requests.post(PLAYLIST_TRACK_ENDPOINT, headers=auth_header).json()


# "https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n/tracks?uris=spoti
# fy%3Atrack%3A4iV5W9uYEdYUVa79Axb7Rh%2Cspotify%3Atrack%3A1301WleyT98MSxVHPZCA6M"
#  -H "Accept: application/json" -H "Content-Type: application/json" -H "Authoriza
#  tion: Bearer BQA5wqZVoVAE97FnRmtI6V5xyHWIZIVk_AhXSHz2c0WAFADG2cRbDMiV2Id-MZUEQc
#  88znG0jRwTBsI4s429uh0XMlCHfjQt2WqLN502aEuvEN0Zf_cGce_FzQKNNsjOdaXDj0ckuV0aedCQ-
#  VbCJYdzNf5-j13YRFBopDFW0w8mxqrPNED5-RD5JabHqih2yMSw2avtugF_dTIWOC9a"
   
# spotify:user:ea.olivia:playlist:0lwpuc5gkYYzu9OIDvOD8M
# PARSE 0lwpuc5gkYYzu9OIDvOD8M
# FORMAT playlist_uri






