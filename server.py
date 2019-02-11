from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from flask_oauthlib.client import OAuth, OAuthException


#from model import connect_to_db, db, User, Movie, Rating

SPOTIFY_APP_ID = ''
SPOTIFY_APP_SECRET = ''


app = Flask(__name__)
app.debug = True
# app.secret_key = 'development'
oauth = OAuth(app)

# spotify = oauth.remote_app(
#     'spotify',
#     consumer_key=SPOTIFY_APP_ID,
#     consumer_secret=SPOTIFY_APP_SECRET,
#     # Change the scope to match whatever it us you need
#     # list of scopes can be found in the url below
#     # https://developer.spotify.com/web-api/using-scopes/
#     request_token_params={'scope': 'user-read-email'},
#     base_url='https://accounts.spotify.com',
#     request_token_url=None,
#     access_token_url='/api/token',
#     authorize_url='https://accounts.spotify.com/authorize'
# )


@app.route('/')
def index():

    return render_template('homepage.html')


@app.route('/login')
def login():
    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)


# @app.route('/login/authorized')
# def spotify_authorized():
#     resp = spotify.authorized_response()
#     if resp is None:
#         return 'Access denied: reason={0} error={1}'.format(
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     if isinstance(resp, OAuthException):
#         return 'Access denied: {0}'.format(resp.message)

#     session['oauth_token'] = (resp['access_token'], '')
#     me = spotify.get('/me')
#     return 'Logged in as id={0} name={1} redirect={2}'.format(
#         me.data['id'],
#         me.data['name'],
#         request.args.get('next')
#     )


# @spotify.tokengetter
# def get_spotify_oauth_token():
#     return session.get('oauth_token')





    # Do not debug for demo
if __name__ == '__main__':
    app.run(host="0.0.0.0")