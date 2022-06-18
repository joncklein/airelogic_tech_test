import musicbrainzngs as mbz
from music_object_class import MusicObject
import requests

class apiRequestor():

    def assign_useragent(self):
        mbz.set_useragent('TheRecordIndustry.io', '0.1')

    def retrieve_artist_details(self, music_object):
        artist_list = mbz.search_artists(query=music_object.artist_name)['artist-list']
        music_object.artist_id = artist_list[0]['id'] 

    def retrieve_release_details(self,music_object):
        release_list = mbz.browse_releases(artist = music_object.artist_id, release_type=['album'])['release-list']
        for release in release_list:
            release_id = release["id"]
            release_track_list = mbz.get_release_by_id(release_id, includes=["recordings"])
            tracks = (release_track_list["release"]["medium-list"][0]["track-list"])
        for i in range(len(tracks)):
            line = (tracks[i])
            music_object.full_track_list.append({line["recording"]["title"]})

#def send_request():

#def retrieve_lyrics():
