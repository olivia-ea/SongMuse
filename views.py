"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

import spotify
import requests
from settings import *
# from model import db, connect_to_db, User, Playlist 

app = Flask(__name__)
app.jinja_env.undefinded = StrictUndefined
app.debug = True


@app.route('/')
def index():

    return render_template('homepage.html')

@app.route('/services-login')
def services_login():
    """Music services login splash page."""

    spotify_auth_url = spotify.auth_page()

    return render_template("/services-login.html", 
                            spotify_auth_url=spotify_auth_url)

# @app.route('/spotify-auth')
# def authorization():
#     """ Spotify Authorization Page """

#     auth_url = spotify.user_auth()
#     return redirect(auth_url)

