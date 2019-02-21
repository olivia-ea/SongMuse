"""Spotify keys"""

import os
# from flask_oauthlib.client import OAuth, OAuthException

# Client keys
SPOTIFY_CLIENT_ID=os.environ['SPOTIFY_APP_ID']
SPOTIFY_CLIENT_SECRET=os.environ['SPOTIFY_APP_SECRET']
SPOTIFY_REDIRECT_URI='http://localhost:5000/spotify-callback'

# Spotify URLs
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_VERSION = 'v1'
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{SPOTIFY_API_VERSION}'
SPOTIFY_SCOPE = 'streaming user-read-birthdate user-read-email user-read-private user-read-birthdate user-modify-playback-state playlist-modify-public playlist-read-collaborative'


auth_query_param = {
    'response_type': 'code',
    'redirect_uri': SPOTIFY_REDIRECT_URI,
    'scope': SPOTIFY_SCOPE,
    'client_id': SPOTIFY_CLIENT_ID
}

