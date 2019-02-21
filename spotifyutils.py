import json
import requests
import sys
import base64
from settings import *
from views import *
from flask import request, flash, session
from model import db, connect_to_db, User, Activity, Playlist, Song, Playlist_Song

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
    """ Returns Spotify's authorization header.
    
    Args: access_token is returned from get_access_token().
    """

    return {"Authorization" : f"Bearer {token}"}


def search_playlists():
    """ Finds the playlist id number from the API response. """ 
    # should take in activity but omitted for demo purposes 

    PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q=workout&type=playlist&limit=5&offset=5")
    # testing

    # PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q=" + activity + "&type=playlist&limit=5&offset=5")
    url = PLAYLIST_ENDPOINT
    token = session['spotify_token']
    response = requests.get(url, headers=auth_header(token)).json()
    playlist_id = (response['playlists']['items'][0]['id'])

    return playlist_id

def search_playlist_tracks():
    """ Finds the tracks based off the id number. """

    playlist_id = search_playlists()

    TRACK_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, "playlists", playlist_id, "tracks?market=US&limit=10&offset=10")
    url = TRACK_ENDPOINT
    token = session['spotify_token']
    response = requests.get(url, headers=auth_header(token)).json()
    track_uri = (response['items'][0]['track']['uri'])
    track_name = (response['items'][0]['track']['name'])
    track_artist = (response['items'][0]['track']['artists'][0]['name'])

    # for i in range(0, len(response)):
    #     track_name = (response['items'][i]['track']['name'])
    #     track_artist = (response['items'][i]['track']['artists'][0]['name'])
    #     track_uri = (response['items'][i]['track']['uri'])
    #     new_song = Track(song_name=track_name, artist_name=track_artist, song_uri=track_uri)
    #     # db.session.add(new_song)
    #     i += 1

    return track_name, track_artist, track_uri
    
def get_user_id():
    """ Return users spotify id to add to database """ 

    token = session['spotify_token']
    headers = auth_header(token)

    request = f'{SPOTIFY_API_URL}/me'
    user_info_data = requests.get(request, headers=headers).json()
    user_id = user_info_data['id']

    return user_id

def create_playlist(auth_header, user_id, playlist_tracks, mood, playlist_name):
    """ Create playlist and add tracks to playlist. """

    # playlist_id 
    # user_id =ForeignKey
    # activity_id = ForeignKey
    # playlist_name = 
    # playlist_uri = 

    # name = f'{playlist_name}'

    # payload = { 
    #     'name' : name,
    #     'description': 'Activity generated playlist'
    #     }

    # USER_PLAYLIST_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, 'users', user_id, 'playlists')
    # url = USER_PLAYLIST_ENDPOINT
    # playlist_data = requests.post(url, data=json.dumps(payload), headers=auth_header).json()
    # playlist_id = playlist_data['id']
    # session['playlist'] = playlist_id

    # playlist_exist = db.session.query(Playlist).filter(Playlist.id == playlist_id).all()

    # if not playlist_exist:
    #     new_playlist = Playlist(id = playlist_id,
    #                             user_id = user_id,
    #                             mood = mood)
    #     db.session.add(new_playlist)


    # # for track in playlist_tracks:
    # #     playlist_track_exist = db.session.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_uri == track).all()
    # #     if not playlist_track_exist:
    #         # new_playlist_track = PlaylistTrack(playlist_id = playlist_id, track_uri = track)
    # #         db.session.add(new_playlist_track)

    # new_playlist_track = PlaylistTrack(playlist_id = playlist_id, track_uri = track)
    # db.session.add(new_playlist_track)


    # db.session.commit()

    # track_uris = '%2C'.join(playlist_tracks)
    # add_tracks = f'{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks?uris={track_uris}'
    # tracks_added = requests.post(add_tracks, headers=auth_header).json()
    # # tracks_added = post_spotify_data(add_tracks, auth_header)

    # return playlist_data['external_urls']['spotify']

    pass



'''
ENDPOINTS:
Search for a playlist:   GET https://api.spotify.com/v1/search
Create a playlist:  POST https://api.spotify.com/v1/playlists
Add tracks to a playlist: POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
Get the playlist: GET https://api.spotify.com/v1/playlists/{playlist_id}

'''





