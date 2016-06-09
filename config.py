from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.playlist
users = db.users
songs = db.songs
history = db.history

SONG_LIMIT = 10
PLAYLIST_SIZE = 100

SECRET_KEY = 'lol'

# Spotify Credentials
SPOTIFY_USERNAME = 'conordowling'
SPOTIFY_ID = '2c3462dae14e4d98a25c37a7717efb9c'
SPOTIFY_SECRET = 'b23df68f58a043858cfdc0186c5658fd'
REDIRECT_URI = 'http://facebook.com'