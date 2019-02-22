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

    PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q=workout&type=playlist&limit=3&offset=3")
    # HARD CODED FOR TESTING WILL CHANGE LATER

    # PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q=" + activity + "&type=playlist&limit=5&offset=5")
    url = PLAYLIST_ENDPOINT
    token = session.get('access_token')
    response = requests.get(url, headers=auth_header(token)).json()
    playlist_id_1 = (response['playlists']['items'][0]['id'])
    # playlist_id_2 = (response['playlists']['items'][1]['id'])
    # playlist_id_3 = (response['playlists']['items'][2]['id'])

    # for i in range(0, len(response)):
    #     playlist_id = (response['playlists']['items'][i]['id'])
    #     i += 1


    return playlist_id_1
    # , playlist_id_2, playlist_id_3

def search_playlist_tracks():
    """ Finds the tracks based off the id number. """

    playlist_id_1= search_playlists()
    # , playlist_id_2, playlist_id_3 
    # needs to take in three playlists

    TRACK_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, "playlists", playlist_id, "tracks?market=US&limit=10&offset=10")
    url = TRACK_ENDPOINT
    token = session.get('access_token')
    response = requests.get(url, headers=auth_header(token)).json()


    for i in range(0, len(response)):
        track_name = (response['items'][i]['track']['name'])
        track_artist = (response['items'][i]['track']['artists'][0]['name'])
        track_uri = (response['items'][i]['track']['uri'])
        new_song = Song(song_name=track_name, artist_name=track_artist, song_uri=track_uri)
        db.session.add(new_song)
        db.session.commit()
        i += 1
    # added 14 songs instead of 10 FIX LATER

    return ('added to DB')
    
def get_user_id(auth_header):
    """ Return users spotify id to add to database """ 

    # Use later to push playlist to user's spotify account

    request = f'{SPOTIFY_API_URL}/me'
    user_info_data = requests.get(request, headers=auth_header).json()
    user_id = user_info_data['id']

    return user_id

def create_playlist(auth_header, user_id, playlist_tracks, playlist_name):
    """ Create playlist and add tracks to playlist. """

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
1. Search for 5 playlists 
2. Get playlists' ID and randomly select 10 tracks
3. Push all tracks to Song table
4. \

ADD TRACKS    https://api.spotify.com/v1/playlists/{playlist_id}/tracks
'''





