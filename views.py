"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests

import spotifyutils
from settings import *
from model import db, connect_to_db, User, Playlist, Song, Playlist_Song 
# DELETED ACTIVITY FROM MODEL BE SURE TO ADD BACK IN

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

    spotify_response_data = spotifyutils.get_access_token()
    session['access_token'] = spotify_response_data.get('access_token')
    session['refresh_token'] = spotify_response_data.get('refresh_token')

    '''
    print(spotify_response_data)

    {'access_token': 'BQDgSUqcuazClu-tfUSCKSwpKBeuwLRNTdW76aicr470cBMJL3KRK2J_yN6TahL
    jpvwa5GnUK3CuPQlctO-p7B41pVVCPkRPwRft9jowupGrOwbzevEJCpaf2IID3zpmiGnvm1ro9N7MW4f
    W2y-ImC6Era65m_Pp1lDkeCyJHTJoOmvL8qC543nhxMVhnfmfoRt-M83aQw', 'token_type': 'Be
    arer', 'expires_in': 3600, 'refresh_token': 'AQBERXBoAdsvdbsT_ZdhjMYmEusNn_kQuUFl
    B-fJIz6yT8d4uLIgLS0g_DnfrZggoFSdR3RikZ3mf4BbK7cxQpRTgqAfCWFJEszX3oDGlouPzm1wciKY4
    eCqCke-uktjjwej3w', 'scope': 'streaming playlist-read-collaborative user-modify-pl
    ayback-state playlist-modify-public user-read-birthdate user-read-email user-rea
    d-private'}
    '''

    return render_template('callback-page.html')

@app.route('/register-new-user', methods=['GET'])
def register_new_user():

    return render_template('register-new-user.html')

@app.route('/sign-up-verification', methods=["POST"])
def register_process():
    """ Register New User """

    username = request.form["new-username"]
    password = request.form["new-password"]

    user = User.query.filter(User.user_id==username).first()

    if user:
        flash("That username is already taken!")
        return redirect("/login-current-user")
    else:
        new_user = User(user_id=username, password=password, refresh_token=session.get('refresh_token'))
        
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.user_id
        session['logged_user'] = {'username': username}

        flash(f"User {username} added.")

        return redirect("/activity-page")

@app.route('/login-current-user', methods=['GET'])
def login_form():

    return render_template("login-page.html")

@app.route('/login-verification', methods=["POST"])
def login_current_user():
    """ Login for Exisiting User """

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.user_id==username).first()

    if user:
        if user.password == password:
            user_id = user.user_id
            session['logged_user'] = {'username': user_id}

            flash("You've successfully logged in!")
            return redirect("/activity-page")
        else:
            flash("The password is incorrect.")
    else:
        flash("That username doesn't exist!")
        return redirect("/register-new-user")

@app.route('/activity-page')
def display_activity():
    """ Activity Page """

    token = session.get('access_token')
    auth_header = spotifyutils.auth_header(token)
    spotify_user_id = spotifyutils.get_user_id(auth_header)
    playlist_name = 'Workout'



    playlists_ids = (spotifyutils.search_playlists('workout'))
    spotifyutils.search_playlists_tracks(playlists_ids)
    spotifyutils.create_playlist(auth_header, spotify_user_id, playlist_name)


    return render_template('activity-page.html')

@app.route('/logout')
def logout():
    """Log out"""

    del session["logged_user"]
    del session['spotify_token']
    flash("Logged Out.")

    return redirect("/")

'''
import pdb; pdb.set_trace()

'''





