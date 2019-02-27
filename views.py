"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify, json, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests

import spotifyutils
from settings import *
from model import db, connect_to_db, User, Playlist, Song, Activity, Playlist_Song 

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
        new_user = User(user_id=username, password=password, auth_token=session.get('access_token'), refresh_token=session.get('refresh_token'))
        
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

@app.route('/activity-page', methods=['GET'])
def route_activity():

    access_token = session.get('access_token')

    return render_template('activity-page.html', auth_header=access_token)

@app.route('/cont-activity-page', methods=["POST"])
def display_activity():
    """ Activity Page """

    activity_query = request.form["activity_query"]
    playlist_name = request.form["playlist_name"]

    user_id = session.get('logged_user')['username']

    new_activity = Activity(activity_name=activity_query, user_id=user_id)
    db.session.add(new_activity)
    db.session.commit()
    activity_id = new_activity.activity_id

    token = session.get('access_token')
    session['auth_header'] = spotifyutils.auth_header(token)

    auth_header = session['auth_header'] 
    spotify_user_id = spotifyutils.get_user_id(auth_header)

    playlists_ids = (spotifyutils.search_playlists(activity_query))
    playlist_id = spotifyutils.create_playlist(auth_header, spotify_user_id, playlist_name, activity_id)
    spotifyutils.search_playlists_tracks(playlists_ids, playlist_id)
    spotifyutils.seed_spotify_playlist(auth_header, playlist_id)

    '''
    activity = Activity.query.order_by('activity_name').filter(Activity.activity_name.ilike('%{}%'.format(search_str))).all()
    pre-seed activity database to avoid errors of non-existant activities 

    '''
    return redirect("/activity-page")

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





