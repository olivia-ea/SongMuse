import json
import requests
import sys
import base64
from settings import *
from views import *
from flask import request, flash, session
from model import db, connect_to_db, User, Activity, Playlist, Song, Playlist_Song

def generate_auth_url():
    """ Return user authorization url. Used in '/spotify-auth' route. """

    spotify_auth_url = (SPOTIFY_AUTH_URL + '?client_id=' + auth_query_param['client_id'] +
                        '&response_type=' + auth_query_param['response_type'] + 
                        '&redirect_uri=' + auth_query_param['redirect_uri'] + 
                        '&scope=' + auth_query_param['scope'])

    return spotify_auth_url

def get_access_token():
    """Return authorization token from Spotify."""

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

def auth_header(access_token):
    """Return Spotify's authorization header.
    
    Args: access_token is returned from get_access_token().
    """

    return {"Authorization" : f"Bearer {access_token}"}

# def search(query, access_token):
#     """Spotify search request and response.
    
#     Args:
#         query (string) - User inputted query.
    
#     Returns a dictionary containing dictionaries with track information 
#     from API response.
#     """

#     query_str = query.replace(" ", "%20").lower()
#     query_str = "q=" + query_str + "&type=track&limit=10"
#     headers = auth_header(access_token)
#     url = f"{SPOTIFY_API_URL}/search?{query_str}"
#     response = requests.get(url, headers=headers).json()
#     response_lst = response['tracks']['items']

#     search_list_data = list(map(search_data_map, response_lst))

#     return search_list_data











    '''
    baseurl + 
    "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10
    &offset=5" -H "Accept: application/json" -H "Content-Type: application/json" 
    -H "Authorization: Bearer BQCBmQO56ymP3zUs3cT7hd6_XBPreLAGoaCFYoPOL5KhRm2vzV
    QoWjtQaPCCFq2EWYJl5zZUXsJ7b10tK46eDZLxplUjzO4TceCS-lRkHDYX4VtZPtZfv6EB4WsOLg
    MP4Qpsnt9I-3J2XZ5MOy_-luIyLrZhvYwvhlSThrrbZh7RkSfFuKH5MtpFFtuyhT8M9RlxcwOJKwBlUuLR6pE"
    '''
# def template_request():

#     response = requests.get(f'{SPOTIFY_API_BASE_URL}/{SPOTIFY_API_VERSION}/search')
#     print(response.json())


'''
>>> payload = {'token' : '****YOUR-TOKEN****'}
>>> url = 'https://www.eventbriteapi.com/v3/categories'
>>> response = requests.get(url, params=payload)
>>> print(response)


https://api.spotify.com/v1/me

curl -X "GET" "https://api.spotify.com/v1/search?q=workout&type=playlist&market
=US&limit=5&offset=5" -H "Accept: application/json" -H "Content-Type: application
/json" -H "Authorization: Bearer BQAL1Jj_za2FZ_8PM07ppn7StxmqOEOfaXcE_LxU9I4k7CL
xsjpJztsKbSedT5edsM0vQXdmin17QzomOQwio6i8MB_0yljOXebiTqf5tEGtJtA37QkZpL1oZ3tVovSUJeHPB7wJ4WSNqVpQ"

use token endpoint

generate token 
what is a header ask mentor
header + token


'''

