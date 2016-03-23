#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://spotipy.readthedocs.org/en/latest/


#
# Export Pandora likes by radio station and create matching spotify playlists containing those liked tracks
# which can be used as seeds for Playlist radio in Spotify.
#
# Will not run out of the box... need to edit the getPandoraLikesHtml function to use a header crafted from 
# your own packet capture.
#

import time
import json
import requests
import os
import urllib
from bs4 import BeautifulSoup

import spotipy
import spotipy.util as util


class Spotdora:
	pandoraTracks = []
	spotifyTracks = []

	outf = None
	spotify = None

	pandoraFilename = "tracks.json"
	spotifyUsername = None

	def parsePandoraTrack(self, div):
		track = {}
		anchors = div.find_all("a")
	
		track["trackName"] = anchors[0].text
		track["artistName"] = anchors[1].text
		track["channelName"] = anchors[2].text
	
		return track

	def findPandoraTracks(self, html):
		soup = BeautifulSoup(html, "html.parser")
		items = soup.find_all("div", {"class":"section"})
		for i in items:
			track = self.parsePandoraTrack(i)
			self.pandoraTracks.append(track)
			js = json.dumps(track)
			# print js
			if self.outf:
				self.outf.write("\t" + js +",\n")

		if self.outf:
			os.fsync(self.outf)

	def openFile(self):
		self.outf  = open(self.pandoraFilename, "wb")
		self.outf.write("[\n")
	
	def closeFile(self):
		self.outf.write("]\n")
		self.outf.close()

	def testPandora(self):
	
		self.openFile()
		html = open("sample.html", "rb").read()
		self.findPandoraTracks(html)
		self.closeFile()
	
	def getPandoraLikesHtml(self, likeStartIndex=0):	
	
		"""
		HTTP Reuqest sniffed from browser while browsing my likes from:
		http://www.pandora.com/profile/likes/steved12
		
		
			http://www.pandora.com/content/tracklikes?likeStartIndex=0&thumbStartIndex=30&webname=steved12&cachebuster=1458685611559

			GET /content/tracklikes?likeStartIndex=0&thumbStartIndex=20&webname=steved12&cachebuster=1458685607679 HTTP/1.1
			Host: www.pandora.com
			Connection: keep-alive
			Accept: */*
			X-Requested-With: XMLHttpRequest
			User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36
			Referer: http://www.pandora.com/profile/likes/steved12
			Accept-Encoding: gzip, deflate, sdch
			Accept-Language: en-US,en;q=0.8
			Cookie: XXXXX=YYYY;WWWWW=ZZZZ


		
		Replicate this query from your own browser packet capture to fetch all likes and store them locally. 
		
		Copy the value of the cookie header into the cookiestr below. I've stripped my actual cookie from this comment. Yours will be much longer.
		Copy the value of the referer header into the referer variable below.
		
		NOTE NOTE NOTE!!!!
		This code doesn't actually terminate at the end of the list, the same results just keep getting appended, so watch the output and then cancel the script... yay!
		"""	
	
		s = requests.Session()
		cookiestr = "XXXXX=YYYY;WWWWW=ZZZZ" # Make sure you've copied your unique cookie from the packet capture here. Omit the Cookie: prefix.
		referer = "http://www.pandora.com/profile/likes/steved12"
		cookies = {}
		pairs = cookiestr.split(";")
		for pair in pairs:
			kv = pair.split("=")
			key = kv[0].strip()
			value = "=".join(kv[1:]).strip()
			cookies[key] = value
	
		s.cookies = requests.utils.cookiejar_from_dict(cookies)
	
		s.headers = {
			"Host": "www.pandora.com",
			"X-Requested-With": "XMLHttpRequest",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
			"Referer": referer,
			"Accept-Encoding": "gzip, deflate, sdch",
			"Accept-Language": "en-US,en;q=0.8"
		}

	
		url = "http://www.pandora.com/content/tracklikes?likeStartIndex=0&thumbStartIndex={}&webname=steved12&cachebuster=1458685611559".format(likeStartIndex)
		response = s.get(url)
		if response.status_code != 200:
			print response.text
			return None

		return response.text


	def pullPandoraTracks(self):
		self.openFile()
		while True:
			html = self.getPandoraLikesHtml(len(self.pandoraTracks))
			if html is None:
				break
			self.findPandoraTracks(html)
			# Don't be evil.
			time.sleep(1)

		self.closeFile()

	def loadPandoraTracks(self):
		self.pandoraTracks = json.loads(open(self.pandoraFilename, "rb").read())
		print "Loaded {} tracks.".format(len(self.pandoraTracks))






	def parseSpotifyTrack(self, result, pandoraTrack):
		track = {}
		if len(result["tracks"]) and len(result["tracks"]["items"]):
			track["trackName"] = result["tracks"]["items"][0]["name"]
			track["artistName"] = result["tracks"]["items"][0]["artists"][0]["name"]
			track["uri"] = result["tracks"]["items"][0]["uri"]
			track["channelName"] = pandoraTrack["channelName"]

			return track
		else:
			print "Failed to find {} in Spotify".format(pandoraTrack)
	def pullSpotifyTracks(self):
		for pandoraTrack in self.pandoraTracks:
			try:
				results = self.spotify.search(q="artist:{} track:{}".format(pandoraTrack["artistName"], pandoraTrack["trackName"]), type="track")
				spotifyTrack = self.parseSpotifyTrack(results, pandoraTrack)
			# print json.dumps(spotifyTrack, indent=2)
				if spotifyTrack:
					self.spotifyTracks.append(spotifyTrack)
			except:
				print "Failed to search for {}".format(pandoraTrack)

	def buildSpotifyPlaylists(self):
		playlists = {}

		self.spotifyPlaylists = self.spotify.user_playlists(self.spotify.current_user()["id"])

		print "Current Spotify Playlists"
		for playlist in self.spotifyPlaylists["items"]:
			playlists[playlist["name"]] = {"id":playlist["id"], "tracks":[]}
			print playlist["name"]

		print "Scanning {} tracks".format(len(self.spotifyTracks))
		for track in self.spotifyTracks:
			channelName = track["channelName"]

			if not len(channelName):
				continue
			
			if channelName not in playlists:
				print "Creating Spotify Playlist {}".format(channelName)
				response = self.spotify.user_playlist_create(spotify.current_user()["id"], channelName, public=False)
			
				playlists[channelName] = {"id":response["id"], "tracks":[]}
			
			playlists[channelName]["tracks"].append(track["uri"])
		


		for k in playlists:
			playlist = playlists[k]
			tracks = playlist["tracks"]
			if len(tracks):
				print "Populating {} with {} tracks".format(k, len(playlist["tracks"]))
				print tracks
				self.spotify.user_playlist_add_tracks(self.spotify.current_user()["id"], playlist["id"], tracks)
	
	

	def authSpotify(self):
		# Too lazy to figure out which scopes are actually needed, so ask for all of them.
		scope = "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email"
		clientId = "9e41ff3d50b54cceaf24cfcf38ea2857"
		clientSecret = "e9acd3ff114043a8b7facd313a842077"
	
		# scope = urllib.quote(scope)
		token = util.prompt_for_user_token(self.spotifyUsername, scope, clientId, clientSecret, "http://localhost")
	
		self.spotify = spotipy.Spotify(auth=token)

	def testSpotify(self):
		results = self.spotify.current_user_saved_tracks()
		for item in results['items']:
			track = item['track']
			print track['name'] + ' - ' + track['artists'][0]['name']	

def main():
	spotdora = Spotdora()
	spotdora.spotifyUsername = raw_input("Spotify email address: ")
	print spotdora.spotifyUsername

	# Uncomment this to capture your Pandora likes after editing the header in getPandoraLikesHtml.
	#pullPandoraTracks()
	
	spotdora.authSpotify()
#	testSpotify()

	# Loads previously captured Pandora likes. This will work after pullPandoraTracks is successful.
	spotdora.loadPandoraTracks()
	spotdora.pullSpotifyTracks()
	spotdora.buildSpotifyPlaylists()

if __name__ == "__main__":
	main()