import applemusicpy
import json
# import os #? I think I can take this out
from .TrackInfo import TrackInfo

class ApplePlaylist:
    def __init__(self, url=None, kid='', team_id='', am_key=''):
        self.pl_url = url
        self.kid = kid
        self.team_id = team_id
        self.am_key = am_key
        self.am_object = None
        self.pl_object = None
        self.pl_name = None
        self.pl_desc = None
        self.tracks = []

    def print_json(self):
        #? method for debugging purposes
        print(json.dumps(self.pl_object, indent=4))
        return
        
    def create_am_object(self):
        self.am_object = applemusicpy.AppleMusic(self.am_key, self.kid, self.team_id)
        
        self.pl_object = self.am_object.playlist(self.pl_url)
        self.pl_name = self.pl_object['data'][0]['attributes']['name']
        self.pl_desc = "" #todo get description
        # self.tracks = self.pl_object['data'][0]['relationships']['tracks']['data']
        
        return
        
    def get_tracks(self):
        for track in self.pl_object['data'][0]['relationships']['tracks']['data']:
            title = track['attributes']['name']
            artist = track['attributes']['artistName']
                
            self.tracks.append(TrackInfo(title, artist))
            
        return self.tracks