import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyCreator:
	def __init__(self, username=None, scope='playlist-modify-public', tracks=[], pl_name="Playlist", pl_desc=""):
		self.sp_username = username
		if self.sp_username == None:
			self.sp_username = input("Enter your Spotify username: ")

		self.sp_scope = scope
		self.sp_token = SpotifyOAuth(scope=self.sp_scope, username=self.sp_username)
		self.sp_object = spotipy.Spotify(auth_manager=self.sp_token)

		self.tracks = tracks
		self.pl_name = pl_name
		self.pl_desc = pl_desc
		if self.pl_desc != "":
			self.pl_desc = self.pl_desc + " "
		self.pl_desc = self.pl_desc + "This playlist was created with PLconvert."
		self.pl_id = None

	def createSpotifyPlaylist(self):

		new_playlist = self.sp_object.user_playlist_create(user=self.sp_username, name=self.pl_name, public=True, description=self.pl_desc)

		self.pl_id = new_playlist['id']

		return

	def addTracks(self):
		# for each track: id = track.find_id(); spotipy.playlist_add_items(id, self.pl_id)
		# self.tracks[0].find_id(self.sp_object)
		track_ids = []
		no_ids = []

		for track in self.tracks:
			t = track.find_sp_id(self.sp_object)
			if t:
				track_ids.append(t)
			else:
				no_ids.append(track)

		self.sp_object.playlist_add_items(self.pl_id, track_ids)

		#? debugging
		print("NO IDS:")
		for track in no_ids:
			print(track.title)
			print(track.artist)
			print()

		print("{} missing songs".format(len(no_ids)))

		return