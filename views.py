"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

import spotifyutils
import requests
from settings import *
from model import db, connect_to_db, User, Activity, Playlist, Song, Playlist_Song 

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

    spotify_auth_url = spotifyutils.generate_auth_url()

    return redirect(spotify_auth_url)

@app.route('/spotify-callback')
def spotify_callback():

    response_data = spotifyutils.get_access_token()
  
    session['spotify_token'] = response_data.get('access_token')

    USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=spotifyutils.auth_header(response_data.get('access_token')))
    print(resp.json())

    # USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
    # url1 = USER_PLAYLISTS_ENDPOINT
    # resp = requests.get(url1, headers=spotifyutils.auth_header(response_data.get('access_token')))
    # print(resp.json())


    return redirect('/')

@app.route('/register-new-user')
def register_new_user():

    return render_template('register-new-user.html')

@app.route('/sign-up-verification', methods=["POST"])
def sign_up_success():

    username = request.form.get("new-username")
    password = request.form.get("new-password")

    # user = db.session.query(User).filter(User.username==username).first()

    if user:
        flash("That username is already taken!")
        return redirect("/register-new-user")
    else:
        new_user = User(username=username)
        
        db.session.add(new_user)
        # db.session.commit()

        user_id = new_user.user_id
        session['logged_user'] = { 'user_id': user_id,
                                    'username': username}

        flash("Sign-up successful!")
        return redirect("/activity-page")

@app.route('/login-current-user')
def login_form():

    return render_template("login-page.html")

@app.route('/login-verification', methods=["POST"])
def login_current_user():

    username = request.form.get("username")
    password = request.form.get("password")

    #user = db.session.query(User).filter(User.username==username).first()

    if user:
        if user.password == password:
            user_id = user.user_id
            session['logged_user'] = {'user_id': user_id,
                                        'username': username}

            flash("You've successfully logged in!")
            return redirect("/activity-page")
        else:
            flash("The password is incorrect.")
    else:
        flash("That username doesn't exist!")
        return redirect("/login-current-user")

@app.route('/activity-page')
def display_activity():

    return render_template('activity-page.html')


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








