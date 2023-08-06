import json
import re

class TrackInfo:
    def __init__(self, title, artist):
        self.title = title.lower()
        self.artist = artist.lower()
        self.sp_id = None
        self.apl_id = None
        
    def find_sp_id(self, sp_object):
        # use spotipy's search() method to get the track's ID
        search_results = sp_object.search(q=self.title+" "+self.artist, limit=5)

        # get _match_format(self.title, self.artist) so we don't have to keep doing it in the for loop
        formatted_title, artist_set = self._match_format(self.title, self.artist) #todo set default values in method definition so we don't have to pass these values
        
        # loop through the search results to find the first one that matches self.title and self.artist
        for i in range(len(search_results['tracks']['items'])):
            r_title = search_results['tracks']['items'][i]['name'].lower()
            #// r_artist = search_results['tracks']['items'][i]['artists'][0]['name'].lower()
            r_artists_json = search_results['tracks']['items'][i]['artists']
            # create list of artist names from json
            r_artists = []
            for a in r_artists_json:
                r_artists.append(a['name'].lower())

            # check if self._match_format(self.title, self.artist) == self._match_format(r_title, r_artists)
            r_formatted_title, r_artist_set = self._match_format(r_title, r_artists)

            # if formatted titles and artists match: set sp_id and return sp_id
            if r_formatted_title == formatted_title and r_artist_set == artist_set:
                self.sp_id = search_results['tracks']['items'][i]['id']
                return self.sp_id
                
        # if this line is reached, no match was found
        return None

    def _match_format(self, title, artists):
        #? REMOVED 4/21/21
        # # if artists is not a list, separate it into a list by splitting by ' & '
        # if type(artists) is not list:
        #     artists = artists.split(' & ')

        # replace square brackets with parens in title
        title = title.replace('[', '(').replace(']', ')')

        #? NEW 4/21/21
        # if artists is a list, turn it into a string joined by ' & '
        if type(artists) is list:
            artists_str = ' & '.join(artists)
        else:
            artists_str = artists
        # replace " and " with " & " for simpler comparisons later
        artists_str = artists_str.replace(' and ', ' & ')
        # turn back into a list by splitting ' & '
        #note: artist names with '&' or 'and' in them will be split into 2 separate names, which is okay
        artist_list = artists_str.split(' & ')

        # set up return values
        #? REMOVED 4/21/21
        # artist_list = artists
        simple_title = title

        #* HANDLE REMIX (parenthetical)
        if 'remix)' in title:
            # feat artist is between '(' and 'remix)'
            i = title.find('remix)') # i is the index of the 'r' in 'remix'
            # if space before 'remix': decrement i
            if title[i-1] == ' ':
                i -= 1
            # find the opening '(' that goes with 'remix)'
            j = i - 1
            while j > 0 and title[j] != '(':
                j -= 1
            # if space before '(': decrement j
            if title[j-1] == ' ':
                j -= 1
            
            # get song title and featured artist
            simple_title = title[:j]
            temp_feat = title[j+2:i]
            artist_list.append(temp_feat)

        #* HANDLE REMIX (hyphen)
        elif 'remix' in title:
            # put i at the index of 'r' in 'remix'
            i = title.find('remix')
            # move j backwards to find '-'
            j = i
            while j > 0 and title[j] != '-':
                j -= 1

            # extract featured artist between '- ' and ' remix'
            temp_feat = title[j+2:i-1]
            # append temp_feat to artist_list
            artist_list.append(temp_feat)
            # get simple title before ' - '
            if title[j-1] == ' ':
                simple_title = title[:j-1]
            else:
                simple_title = title[:j]

        #* HANDLE FEAT (parenthetical)
        if '(feat.' in simple_title:
            # get index of '(' in '(feat.'
            i = simple_title.find('(feat.')
            # split into two separate strings
            feat_string = simple_title[i:]
            if simple_title[i-1] == ' ':
                simple_title = simple_title[:i-1]
            else:
                simple_title = simple_title[:i]

            # extract featured artist(s) from feat_string between '(feat. ' and ')'
            i = 7 # this puts i at the first letter of the featured artist name
            # use j to find closing paren
            j = i + 1
            while j < len(feat_string) - 1 and feat_string[j] != ')':
                j += 1
            # append to artist_list
            temp_feat = feat_string[i:j]
            artist_list.append(temp_feat)
            
            #? NEW 4/21/21
            # if j is not the last char of feat_str: append the rest of feat_str to simple_title
            j += 1 # now j is one char past ')'
            if j < len(feat_string):
                simple_title = simple_title + feat_string[j:]

        #? NEW 4/21/21
        #* HANDLE FEAT (HYPHENATED)
        elif ' - feat. ' in simple_title:
            i = simple_title.find(' - feat. ')
            temp_feat = simple_title[i+9:] # bc ' - feat. ' is 9 chars long
            simple_title = simple_title[:i]
            artist_list.append(temp_feat)

        #? REMOVED 4/21/21
        # # append artists to artist_list
        # artist_list = artist_list + artists

        #* HANDLE PARENS AND HYPHENS
        simple_title = simple_title.replace('- ', '').replace('(', '').replace(')', '')

        # remove periods, exclamations, and commas from all artists
        for i in range(len(artist_list)):
            artist_list[i] = artist_list[i].replace('.', '').replace('!', '').replace(',', '')

        # return simple_title and a set of artist_list (to avoid repeats)
        return simple_title, set(artist_list)