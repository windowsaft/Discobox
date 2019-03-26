#by windows
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from time import sleep

username = "YOUR USERNAME"
scope = "YOUR SCOPES" #eg: 'user-read-private, user-read-playback-state, user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username,scope,client_id='YOUR CLIENT ID',client_secret='YOUR CLIENT SECRET',redirect_uri='YOUR REDIRECT URL') # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)
# Get current device
devices = spotifyObject.devices()
deviceID = devices["devices"][0]["id"]

def createTxt(txt):
	global file_name
	f = open(file_name,"w+")
	f.write(txt)
	f.close()
	return file_name

def intro():
	global displayName, followers, spotifyObject
	user = spotifyObject.current_user()
	displayName = user['display_name']
	followers = user['followers']['total']
	
	# Welcome
	print()
	print(">>> Welcome to Spotipy " + displayName + "!")
	print(">>> You have " + str(followers) + " followers")
	pass

	# Current track information
	track = spotifyObject.current_user_playing_track()
	if not track:
		print()
		pass
	else:
		artist = track["item"]["artists"][0]["name"]
		track = track["item"]["name"]
		if artist != "":
				print(">>> Currently playing " + artist +  " - " + track)
				print()

def menu():
	print("1 - Search for an artist")
	print("2 - Serach for an album")
	print("3 - Search for a song")
	print("4 - Change volume")
	print("5 - exit")
	print()


def searchArtist():
	global choice
	# Search for artist
	print()
	searchQuery = input("Ok, what's their name?: ")
	print()
	# Get search results
	searchResults = spotifyObject.search(searchQuery,1,0,"artist")
	print(json.dumps(searchResults, sort_keys=True, indent=4))

	# Artist details
	artist = searchResults['artists']['items'][0]
	print(artist["name"])
	print(str(artist["followers"]["total"]) + " followers")
	
	# Get the genres
	item =  artist["genres"]
	x = 0
	genres = []
	for a in item:
		genres.append(item[x])
		x = x + 1
	x = 0
	# Check if the list is empty
	if not genres:
		print("")
		
	else:
		print("Genres:")
		for genre in genres:
			print("    " + genre)

	print()
	webbrowser.open(artist["images"][0]["url"])
	artistID = artist["id"]
	
	# Album and track details
	trackURIs = []
	trackArt = []
	z = 0
	# Extract album data
	albumResults = spotifyObject.artist_albums(artistID)
	albumResults = albumResults["items"]

	for item in albumResults:
		print("ALBUM " + item["name"])
		albumID = item['id']
		albumArt = item["images"][0]["url"]

		#Extract track data
		trackResults = spotifyObject.album_tracks(albumID)
		trackResults = trackResults["items"]
			
		for item in trackResults:
			print(str(z) + ": " + item["name"])
			trackURIs.append(item["uri"])
			trackArt.append(albumArt)
			z+=1
		print()
			

	# See album art and play song
	songSelection = input("Enter a song number to see the album art and play song associated with it (x to exit): ")
	if songSelection == "x":
		print()
		pass
		
	else:
		trackSelectionList = []
		trackSelectionList.append(trackURIs[int(songSelection)])
		spotifyObject.start_playback(deviceID, None, trackSelectionList) # added
		webbrowser.open(trackArt[int(songSelection)])
		print()
		pass

def searchSong():
	# Search for song
	print()
	searchQuery = input("Ok, what's the name of the song?: ")
	print()

	# Get search results
	searchResults = spotifyObject.search(searchQuery,1,0,"track")
	#print(json.dumps(searchResults, sort_keys=True, indent=4))

	# Artist details
	track = searchResults['tracks']['items'][0]
	album = searchResults["tracks"]["items"][0]["album"]
	trackID = track["id"]
	trackURIs = track["uri"]

	# Print song details
	print("Track name:   " + track["name"])
	print("Artist:       " + track["artists"][0]["name"])
	print("Album:        " + album["name"])
	print("Release date: " + album["release_date"])
	print("Popularity:   " + str(track["popularity"]))
	audioAnalysis = spotifyObject.audio_analysis(trackID)
	#	print(json.dumps(audioAnalysis, sort_keys=True, indent=4))
	file_name = track["name"] + "_audioAnalysis.json"
	#createTxt(json.dumps(str(audioAnalysis), sort_keys=True, indent=4))
	item =  audioAnalysis["bars"]
	# Get the beat's start time
	x = 0
	beatsStart = []
	for a in item:
		beatsStart.append(item[x]["start"])
		x = x + 1
	print(beatsStart)
	x = 0

	# Get the beat's duration
	beatsDuration = []
	for a in item:
		beatsDuration.append(item[x]["duration"])
		x = x + 1
	print(beatsDuration)
	x = 0

	# Play Song?
	songPlay = input("Play song? y/n: ")
	if songPlay == "n":
		print()
		pass

	else:
		trackSelectionList = []
		trackSelectionList.append(trackURIs)
		spotifyObject.start_playback(deviceID, None, trackSelectionList) # added
		print()
			
		#Starting the vizualizer
		print(len(beatsStart))
		print(x)
		while x != len(beatsStart):
			while x > 0 and x != (len(beatsStart) - 1):
				print(round(beatsStart[x] - (beatsStart[x - 1] + beatsDuration[x - 1]), 4))
				sleep(round(beatsStart[x] - (beatsStart[x - 1] + beatsDuration[x - 1]), 4))
				print("up" + str(x))
				sleep(beatsDuration[x])
				print("down" + str(x))
				x = x + 1
			sleep(beatsStart[x])
			print("up" + str(x))
			sleep(beatsDuration[x])
			print("down" + str(x))
			x = x + 1
		

def searchAlbum():
	# Search for Albums
	print()
	searchQuery = input("Ok, what's the name of the album?: ")
	print()

	# Get search results
	searchResults = spotifyObject.search(searchQuery,1,0,"album")
	print(json.dumps(searchResults, sort_keys=True, indent=4))
	album = searchResults['albums']['items'][0]
	artist = searchResults['albums']['items'][0]['artists'][0]

	# Print Album details
	print("Album name:   " + album["name"])
	print("Artist:       " + artist['name'])
	print("Release date: " + album["release_date"])
	print()

def changeVolume():
	# Change Spotify volume
	changeVolume = input("Set the percentage for the volume: ")
	spotifyObject.volume(int(changeVolume), deviceID)
	print()
