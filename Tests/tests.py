import pytest
from unittest.mock import patch

from song import Song
from api import MusicBrainzArtistAPI, OVHLyricsAPI, NoSuchArtist



class MockArtistAPIResponse:
    def set_useragent(self, *args, **kwargs):
        pass

    def search_artists(self, *args, **kwargs):
        artist_list = {'artist-list': [{'id': '12345'}]}
        return artist_list

    def browse_releases(self, *args, **kwargs):
        release_list = {'release-list':[{'id': '6789'}]}
        return release_list

    def get_release_by_id(self, *args, **kwargs):
        release_track_list = {
            'release': {
                'medium-list': [{'track-list': [ {'recording':{'title': 'song title'}}]}]}}
        return release_track_list

class MockArtistAPIBadResponse:
    def set_useragent(self, *args, **kwargs):
        pass

    def search_artists(self, *args, **kwargs):
        artist_list = {'artist-list': []}
        return artist_list

class MockLyricAPIResponse:
    def get(self, *args):
        return self

    def json(self, *args):
        return {"lyrics": "some test lyrics"}

class MockLyricAPIBadResponse:
    def get(self, *args):
        return self

    def json(self, *args):
        return {"error": "lyrics not found"}

def test_song_len():
    """Test the length method of the song class"""
    test_song = Song("test artist", "test song", ['some', 'test', 'lyrics'])
    assert len(test_song) == len(['some', 'test', 'lyrics'])

@patch("api.requests", MockLyricAPIResponse())
def test_call_request_song_found_lyrics():
    """Test that songs can be created with lyrics"""
    lyrics_api = OVHLyricsAPI()
    song = Song("test artist", "test song", ['some', 'test', 'lyrics'])
    test_song = lyrics_api.request_song("test artist", "test song")
    assert test_song == song

@patch("api.requests", MockLyricAPIBadResponse())
def test_call_request_song_lyrics_not_found():
    """Test that songs are returned as None if the LyricsAPI value is not as expected"""
    lyrics_api = OVHLyricsAPI()
    test_song = lyrics_api.request_song("test artist", "test song")
    assert test_song == None


@patch("api.mbz", MockArtistAPIResponse())
def test_look_up_artist_id():
    """Test that artist id can be retrieved"""
    artist_api = MusicBrainzArtistAPI(app_name='test', version='0.1', author='test_author')
    test_id = artist_api._look_up_artist_id("test artist")
    assert test_id == '12345'

@patch("api.mbz", MockArtistAPIBadResponse())
def test_look_up_artist_id_artist_not_found():
    """Test that the correct exception is raised when artist not found"""
    artist_api = MusicBrainzArtistAPI(app_name='test', version='0.1', author='test_author')
    with pytest.raises(NoSuchArtist):
        artist_api._look_up_artist_id("test artist")


@patch("api.mbz", MockArtistAPIResponse())
def test_look_up_song_names():
    """Test that song titles can be retrieved"""
    artist_api = MusicBrainzArtistAPI(app_name='test', version='0.1', author='test_author')
    artist_id = '12345'
    song = {'song title'}
    test_songs = artist_api._look_up_song_names(artist_id)
    assert test_songs == song
