"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from spotifyutils import *
import requests
from settings import *
# from model import db, connect_to_db, User, Playlist 

app = Flask(__name__)
app.jinja_env.undefinded = StrictUndefined
app.debug = True

@app.route('/')
def index():
    """ Homepage """

    return render_template('homepage.html')

@app.route('/spotify-login')
def spotify_login():
    """ Spotify Authorization Page """

    spotify_auth_url = generate_auth_url()

    return redirect(spotify_auth_url)

@app.route('/spotify-callback')
def spotify_callback():

    response_data = get_access_token()
  
    session['spotify_token'] = response_data.get('access_token')


    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')

    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header(response_data.get('access_token')))
    print(resp.json())


    return redirect('/')

# @app.route('/activity-page')
# def issuing_token():

#     access_token = session['spotify_token']

#     query = request.args.get("userquery")

#     spotify_data = spotify.search(query, access_token)
   
#     return jsonify({'spotify': spotify_data})


# USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
# def get_users_profile(auth_header):
#     url = USER_PROFILE_ENDPOINT
#     resp = requests.get(url, headers=auth_header)
#     return resp.json()



# GET_ARTIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'artists') 


# def get_users_recently_played(auth_header):
#     url = USER_RECENTLY_PLAYED_ENDPOINT
#     resp = requests.get(url, headers=auth_header)
#     return resp.json()




'''


import pdb; pdb.set_trace()

response = requests.get(url)
return response.json()

API ENDPOINTS

Get a Playlist
/v1/playlists/{playlist_id}
GET
Returns: playlist

Create a Playlist
POST
/v1/users/{user_id}/playlists

Add Tracks to a Playlist
POST
/v1/playlists/{playlist_id}/tracks


SEARCH FOR A PLAYLIST USING STRING
https://api.spotify.com/v1/search

'''








