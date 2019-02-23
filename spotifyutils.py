import json
import requests
import sys
import base64
from settings import *
from views import *
from flask import request, flash, session
from model import db, connect_to_db, User, Playlist, Song, Playlist_Song
# DELETED ACTIVITY FROM MODEL BE SURE TO ADD BACK

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

def search_playlists(activity):
    """ Finds the playlist id numbers from the API response. """ 

    PLAYLIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "search?q="+ activity +"&type=playlist&limit=3&offset=3")
    url = PLAYLIST_ENDPOINT
    token = session.get('access_token')
    response = requests.get(url, headers=auth_header(token)).json()

    playlists_ids = []
    for i in range(0, 3):
        playlist_id = (response['playlists']['items'][i]['id'])
        playlists_ids.append(playlist_id)

    return playlists_ids

def search_playlists_tracks(playlists_ids):
    """ Finds the tracks based off the id number. """

    playlist_1, playlist_2, playlist_3 = playlists_ids

    for playlist_id in playlists_ids:
        TRACK_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, "playlists", playlist_id, "tracks?market=US&limit=10&offset=10")
        url = TRACK_ENDPOINT
        token = session.get('access_token')
        response = requests.get(url, headers=auth_header(token)).json()
        for i in range(0, 10):
            track_name = (response['items'][i]['track']['name'])
            track_artist = (response['items'][i]['track']['artists'][0]['name'])
            track_uri = (response['items'][i]['track']['uri'])
            new_song = Song(song_name=track_name, artist_name=track_artist, song_uri=track_uri)
            db.session.add(new_song)
            db.session.commit()

    # NESTED FOR-LOOP TO ADD 30 SONGS TO DATABASE -- WILL FIX LATER BUT WORKS FOR NOW

    return ('Added to DB.')
    
def get_user_id(auth_header):
    """ Return users spotify id to add to database """ 

    request = f'{SPOTIFY_API_URL}/me'
    user_info_data = requests.get(request, headers=auth_header).json()
    user_id = user_info_data['id']

    return user_id

def create_playlist(auth_header, spotify_user_id, playlist_name):
    """ Create playlist and add tracks to playlist. """

    '''
    {'collaborative': False, 'description': 'Activity generated playlist', 
    'external_urls': {'spotify': 'https://open.spotify.com/playlist/6siGcW66hhE
    FVN18L7rY3o'}, 'followers': {'href': None, 'total': 0}, 'href': 'https://ap
    i.spotify.com/v1/playlists/6siGcW66hhEFVN18L7rY3o', 'id': '6siGcW66hhEFVN18L
    7rY3o', 'images': [], 'name': 'Workout', 'owner': {'display_name': 'ea.olivi
    a', 'external_urls': {'spotify': 'https://open.spotify.com/user/ea.olivia'}, 
    'href': 'https://api.spotify.com/v1/users/ea.olivia', 'id': 'ea.olivia', 't
    ype': 'user', 'uri': 'spotify:user:ea.olivia'}, 'primary_color': None, 'pub
    lic': True, 'snapshot_id': 'MSxmOWEyZWU5NzRiNjlmMzEwYjM1YmQ0MDAyNDA3MmNkM2
    U5MWQzZjMy', 'tracks': {'href': 'https://api.spotify.com/v1/playlists/6si
    GcW66hhEFVN18L7rY3o/tracks', 'items': [], 'limit': 100, 'next': None, 'off
    set': 0, 'previous': None, 'total': 0}, 'type': 'playlist', 'uri': 'spotify
    :user:ea.olivia:playlist:6siGcW66hhEFVN18L7rY3o'}
    '''
    payload = { 
        'name' : playlist_name
        # 'description': description
        }

    USER_PLAYLIST_ENDPOINT = "{}/{}/{}/{}".format(SPOTIFY_API_URL, 'users', spotify_user_id, 'playlists')
    url = USER_PLAYLIST_ENDPOINT
    playlist_data = requests.post(url, data=json.dumps(payload), headers=auth_header).json()
    playlist_uri = playlist_data['uri']
    user_id = session.get('logged_user')['username']


    # session['playlist'] = playlist_id

    playlist_exist = db.session.query(Playlist).filter(Playlist.playlist_uri == playlist_uri).all()

    if not playlist_exist:
        new_playlist = Playlist(playlist_name = playlist_name,
                                user_id = user_id,
                                playlist_uri = playlist_uri)
        db.session.add(new_playlist)
        db.session.commit()


    # for track in playlist_songs:
    #     playlist_song_exist = db.session.query(Playlist_Song).filter(Playlist_Song.playlist_id == playlist_id, PlaylistTrack.track_uri == track).all()
    #     if not playlist_track_exist:
    #         new_playlist_song = Playlist_Song(playlist_id = playlist_id, song_uri = track)
    #         db.session.add(new_playlist_song)

    # new_playlist_song = PlaylistTrack(playlist_id = playlist_id, song_uri = track)
    # db.session.add(new_playlist_track)


    # db.session.commit()

    # track_uris = '%2C'.join(playlist_tracks)
    # add_tracks = f'{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks?uris={track_uris}'
    # tracks_added = requests.post(add_tracks, headers=auth_header).json()
    # # tracks_added = post_spotify_data(add_tracks, auth_header)

    return playlist_data['external_urls']['spotify']





