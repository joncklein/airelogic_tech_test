import pytest
from unittest.mock import patch
import html
import requests

from song import Song
from api import MusicBrainzArtistAPI, OVHLyricsAPI, NoSuchArtist

artist_name = "fake artist"
song_name = "fake song"
lyrics = "some fake lyrics"
lyric_list = ['some', 'fake', 'lyrics']
fake_song = Song(artist_name, song_name, lyric_list)
fake_lyrics_api = OVHLyricsAPI()
fake_artist_api = MusicBrainzArtistAPI(app_name='test', version='0.1', author='test_author')

class MockArtistAPIResponse:
    def set_useragent():
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
    def set_useragent():
        pass

    def search_artists(self, *args, **kwargs):
        artist_list = {'artist-list': []}
        return artist_list

class MockLyricAPIResponse:
    def get(self, *args):
        return self

    def json(self, *args):
        return {"lyrics": f"{lyrics}"}

class MockLyricAPIBadResponse:
    def get(self, *args):
        return self

    def json(self, *args):
        return {"error": "lyrics not found"}

def test_song_len():
    assert len(fake_song) == len(lyric_list)


def test_build_lyrics_url():
    lyrics_api_base = "https://api.lyrics.ovh/v1"
    correct_string = html.escape(f"{lyrics_api_base}/{artist_name}/{song_name}")
    assert fake_lyrics_api._build_lyrics_url(artist_name, song_name) == correct_string

@patch("api.requests", MockLyricAPIResponse())
def test_call_request_song_found_lyrics():
    test_song = fake_lyrics_api.request_song(artist_name, song_name)
    assert fake_song == test_song

@patch("api.requests", MockLyricAPIBadResponse())
def test_call_request_song_lyrics_not_found():
    with pytest.raises(KeyError, ValueError):
        fake_lyrics_api.request_song(artist_name, song_name)
    
@patch("api.requests", MockLyricAPIResponse())
def test_call_request_song_lyrics_404():
    with pytest.raises(requests.exceptions.HTTPError):
        fake_lyrics_api.request_song(artist_name, song_name)

def test_request_songs():
    """test to request song from lyric api"""


@patch("api.mbz", MockArtistAPIResponse())
def test_look_up_artist_id():
    test_id = fake_artist_api._look_up_artist_id(artist_name)
    assert test_id == '12345'

@patch("api.mbz", MockArtistAPIBadResponse())
def test_look_up_artist_id_artist_not_found():
    with pytest.raises(NoSuchArtist):
        fake_artist_api._look_up_artist_id(artist_name)


@patch("api.mbz", MockArtistAPIResponse())
def test_look_up_song_names():
    artist_id = '12345'
    fake_song = {'song title'}
    test_songs = fake_artist_api._look_up_song_names(artist_id)
    assert test_songs == fake_song
