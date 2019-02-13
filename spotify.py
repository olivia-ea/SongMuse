import json
import requests
import sys
import base64
import urllib
from settings import *
from flask import request, flash, session
# from model import User Playlist, db, connect_to_db

def get_user_authorization():
    """ Return user authorization url. """

    url_args = '&'.join(['{}={}'.format(key,urllib.parse.quote(val)) for key,val in auth_query_param.items()])
    auth_url = f'{SPOTIFY_AUTH_URL}/?{url_args}'
    return auth_url

