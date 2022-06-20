from abc import ABCMeta, abstractmethod
import musicbrainzngs as mbz
import html
import requests
import string
from typing import TYPE_CHECKING, Dict, Iterator, List

from artist import Artist
from song import Song
from exceptions import NoSuchArtist

class AbstractArtistAPI(metaclass=ABCMeta):
    """An abstract implementation of the proper API."""

    @abstractmethod
    def look_up_artist(self, artist_name: str) -> Iterator[Artist]:
        """Look up an artist, yielding possible matches."""

    @abstractmethod
    def look_up_releases(self, artist: Artist) -> Iterator[Artist]:
        """retrieve releases from api"""

class RealArtistAPI(AbstractArtistAPI):

    def __init__(self, useragent: list):
        self.useragent = useragent

    def assign_useragent(self):
        mbz.set_useragent(self.useragent[0], self.useragent[1])

    def look_up_artist(self, artist: Artist) -> Iterator[Artist]:
        artist_list = mbz.search_artists(query=artist.artist_name)['artist-list']
        artist.artist_id = artist_list[0]['id'] 
        return artist

    def look_up_releases(self, artist: Artist) -> Iterator[Artist]:
        release_list = mbz.browse_releases(artist=artist.artist_id, release_type=['album'])['release-list']
        for release in release_list:
            release_id = release["id"]
            release_track_list = mbz.get_release_by_id(release_id, includes=["recordings"])
            tracks = (release_track_list["release"]["medium-list"][0]["track-list"])
            for track in tracks:
                song = Song(song_name=track["recording"]["title"]) 
                artist.full_tracklist.append(song)
        return artist

class FakeArtistAPI(AbstractArtistAPI):
    """
    A fake API request to use for testing. This can be primed with
    artists to look up.

    """

    def __init__(self, fake_artists: Dict[str, List[Artist]]):
        self.fake_artists = fake_artists

    def look_up_artist(self, artist_name: str) -> Iterator[Artist]:
        if artist_name not in self.fake_artists:
            raise NoSuchArtist(artist_name)

        yield from self.fake_artists[artist_name]

class AbstractLyricsAPI(metaclass=ABCMeta):
    """An abstract implementation of the proper API."""

    @abstractmethod
    def build_lyrics_url(self, artist_name: str, song_name: str) -> str:
        """build lyrics url"""

    def request_lyrics(self, url: str, song: Song) -> Iterator[Song]:
        """retrieve lyrics from api"""

class RealLyricsAPI(AbstractLyricsAPI):

    def build_lyrics_url(self, artist_name: str, song_name: str) -> str:
        lyrics_api_base = 'https://api.lyrics.ovh/v1'
        lyrics_api_url = html.escape(f'{lyrics_api_base}/{artist_name}/{song_name}')
        return lyrics_api_url

    def request_lyrics(self, url: str, song: Song) -> Iterator[Song]:
        try:
            response = requests.get(url)
            lyrics = response.json()['lyrics']
            song.lyrics = lyrics.translate(str.maketrans('', '', string.punctuation)).split()
            return song
        except requests.exceptions.HTTPError:
            pass

class FakeLyricsAPI(AbstractLyricsAPI):
    def build_lyrics_url(self, artist_name: str, song_name: str) -> str:
        lyrics_api_base = 'https://api.lyrics.ovh/v1'
        lyrics_api_url = html.escape(f'{lyrics_api_base}/{artist_name}/{song_name}')
        return lyrics_api_url

    def request_lyrics(self, url: str, song: Song) -> Iterator[Song]:
        try:
            response = requests.get(url)
            lyrics = response.json()['lyrics']
            song.lyrics = lyrics.translate(str.maketrans('', '', string.punctuation)).split()
            return song
        except requests.exceptions.HTTPError:
            pass