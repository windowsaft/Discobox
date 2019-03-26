
import os
import sys
import json
import spotipy
import webbrowser
from time import sleep
import spotipy.util as util
from json.decoder import JSONDecodeError
from resources import *

def main():
	intro()

	while True:
		menu()
		choice = input("Your choice: ")

		# Search for an artist
		if choice == "1":
			searchArtist()
		
		# Search for an album
		if choice == "2":
			searchAlbum()
			
		# Search for a song
		if choice == "3":
			searchSong()

		# Change volume
		if choice == "4":
			changeVolume

		# End the program
		if choice == "5":
			exit()

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

# User information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

main()
