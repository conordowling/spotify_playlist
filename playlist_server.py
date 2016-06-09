from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect

import spotipy

import pymongo
from config import *

app = Flask(__name__)

app.secret_key = SECRET_KEY
@app.route('/')
def hello_world():
	votes = []
	if 'user_id' in session:
		user = users.find_one({ "user_id": session['user_id'] })
		if user:
			votes = user["votes"]
	print session
	return render_template('playlist.html', trending=get_vote_counts(), votes=votes)

@app.route('/login/<user_id>')
def login(user_id):
	session['user_id'] = user_id
	session['logged_in']= True
	print "logging in"
	print session
	return redirect('/')

@app.route('/logout')
def logout():
	session.pop('user_id')
	session['logged_in'] = False
	return redirect('/')

@app.route('/playlist')
def get_playlist():
	if 'user_id' in session:
		pass
	return 'playlist'

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/history')
def history():
	return render_template('history.html')

##################
# VOTE FUNCTIONS #
##################

def get_vote_counts():
	return songs.find().sort("votes", pymongo.DESCENDING)[:10]


def get_votes(user_id):
	user = users.find_one({'user_id':user_id})
	return user['songs']

@app.route('/vote', methods=['POST', 'GET'])
def vote_route():
	return str(vote(request.form['userID'], request.form['songID']))

def vote(user_id, song_id):
	song = sp.track(song_id)
	print song
	user = users.find_one({'user_id':user_id})
	if not user:
		user = { 'id': user_id, 'votes':[song] }
		users.insert(user)
		return True

	if len(user['votes']) < SONG_LIMIT and song['id'] not in [ i['id'] for i in user['votes'] ]:
		user['votes'].append(song)
		# update song db
		vote_count = songs.find_one( { 'id':song['id'] })
		if vote_count:
			vote_count["votes"] += 1
			songs.find_one_and_replace({'id':song['id']}, vote_count)
		else:
			vote_count = song
			vote_count['votes'] = 1
			songs.insert(vote_count)

		users.find_one_and_replace({'user_id':user_id}, user)
		return True
	return False

@app.route('/unvote', methods=['POST', 'GET'])
def unvote_route():
	return str(unvote(request.form['userID'], request.form['songID']))

def unvote(user_id, song_id):
	user = users.find_one({'user_id':user_id})
	if not user:
		print 'there is no such user'
		return False

	if song_id in [ i['id'] for i in user['votes'] ]:
		user['votes'] = [x for x in user['votes'] if x['id'] != song_id]
		users.update({'user_id':user_id}, user)
		# update song db
		vote_count = songs.find_one({'id':song_id})
		if not vote_count:
			print "no record of vote"
			return False
		vote_count["votes"] -= 1
		songs.update({'id':song_id}, vote_count)
		return True

	print 'there is no such song'
	return False

######################
# PLAYLIST FUNCTIONS #
######################

sp = spotipy.Spotify()

def authenticate():
	scopes = 'playlist-modify-public'
	spotipy.util.prompt_for_user_token( SPOTIFY_USERNAME, 
										scope=scope, 
										client_id=SPOTIFY_ID, 
										client_secret=SPOTIFY_SECRET, 
										redirect_uri=REDIRECT_URI
									  )

def get_playlist(playlist):
	pass	


def add_song(playlist, song):
	sp.user_playlist_add_tracks()

def remove_song(playlist, song):
	pass

def update_playlist():
	pass


if __name__ == '__main__':
	app.debug = True
	app.run()