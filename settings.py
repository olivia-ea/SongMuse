"""Spotify keys"""
import os
from flask_oauthlib.client import OAuth, OAuthException


# Client keys
CLIENT_ID=os.environ['SPOTIFY_APP_ID']
CLIENT_SECRET=os.environ['SPOTIFY_APP_SECRET']
REDIRECT_URI=os.environ['SPOTIFY_REDIRECT_URI']
