import json
import requests
import sys
import base64
import urllib
from settings import *
from flask import request, flash, session
# from model import User Playlist, db, connect_to_db

# Spotify URLs
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
SPOTIFY_API_VERSION = 'v1'
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{SPOTIFY_API_VERSION}'
SPOTIFY_SCOPE = 'streaming user-read-birthdate user-read-email user-read-private user-modify-playback-state'

auth_query_param = {
    'response_type': 'code',
    'redirect_uri': SPOTIFY_REDIRECT_URI,
    'scope': SPOTIFY_SCOPE,
    'client_id': SPOTIFY_CLIENT_ID
}

def get_user_authorization():
    """ Return user authorization url. """

    url_args = '&'.join(['{}={}'.format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = f'{SPOTIFY_AUTH_URL}/?{url_args}'
    return auth_url

@app.route('/services-login')
def services_login():
    """Music services login splash page."""

    # spotify_auth_url = spotify.auth_page()

    return render_template("/services-login.html", 
                            spotify_auth_url=spotify_auth_url)



