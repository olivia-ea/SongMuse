# SongMuse
SongMuse is a full stack web app that uses the Spotify API to generate playlists. 

## Table of Contents
* Tech Stack 
* [Setting Up/Installation](#https://github.com/olivia-ea/SongMuse#installation)
* [Demo](#https://github.com/olivia-ea/SongMuse#demo)


## Tech Stack
* Frontend: HTML5, JavaScript, Jinja, jQuery, Bootstrap 
* Backend: Python, Flask, PostgreSQL, SQLAlchemy 
* APIs: Spotify

## Setting Up/Installation 

To run SongMuse on local computer, follow the below steps:

Clone repository: 
```
$ https://github.com/olivia-ea/SongMuse.git
```

Set up virtual environment: 

```
$ virtualenv env
```

Activate virtual envirnoment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip install -r requirements.txt
```

Get Client ID and Client Secret from Spotify and save them to a file secrets.sh:
```
export SPOTIFY_CLIENT_SECRET=YOUR_KEY
export SPOTIFY_CLIENT_ID=YOUR_KEY
```

Create database 'users':
```
$ createdb users
```

Create your database tables:
```
$ python3 models.py
```

Run from the command line:
```
$ python3 server.py
```

Open localhost:5000 on browser.



