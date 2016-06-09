import spotipy
import pymongo
from pymongo import MongoClient

song_ids = [
				'70eDxAyAraNTiD6lx2ZEnH',
				'6aEgrTRLSRQ0FIrvOwcOE6',
				'0sxNfiTrUFBqMSJ92EmijP',
				'3CtZB2dVuHWHXIGShH9jUK',
				'2dLLR6qlu5UJ5gk0dKz0h3',
				'3lO38SiB2WAQRqTAHN7WTC',
				'1x5M7e748IC3LOejjvdOia',
				'34v7Zs9a64h1xC3PWrmypP',
				'5PUawWFG1oIS2NwEcyHaCr',
				'6C7ZgThn6Yan5MTZdAEEFw'
			]

vote_counts = [121,43,12,10,8,7,7,6,5,0]

sp = spotipy.Spotify()

songs = sp.tracks(song_ids)


client = MongoClient()

#create test user
user_db = client.playlist.users

user_db.drop()

user_db.insert({"user_id":"10154316818652859", "votes":[ songs["tracks"][0], songs["tracks"][1] ]})

# create test votes
vote_db = client.playlist.songs
vote_db.drop()


for song in songs["tracks"]:
	song["votes"] = vote_counts.pop()
	vote_db.insert(song)

# TO DO: Create indices