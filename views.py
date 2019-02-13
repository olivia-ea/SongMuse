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
    """ Homepage """
    return render_template('homepage.html')

@app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """

    auth_url = spotify.get_user_authorization()
    
    return redirect(auth_url)

@app.route('/spotify-callback')
def doesthiswork():
    return redirect('/')