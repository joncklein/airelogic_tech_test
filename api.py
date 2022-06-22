import html
import string
from typing import Iterator, Optional, Set

import musicbrainzngs as mbz
import requests

from artist import Artist
from song import Song


class NoSuchArtist(KeyError):
    """Error to raise if an artist can't be found."""


class MusicBrainzArtistAPI:
    """An implementation for the API for MusicBrainz."""

    def __init__(self, app_name: str, version: str, author: str):
        mbz.set_useragent(app_name, version, author)

    @staticmethod
    def _look_up_artist_id(artist_name: str) -> str:
        """Look up the id of the artist in MusicBrainz."""
        artist_list = mbz.search_artists(query=artist_name)["artist-list"]
        try:
            return artist_list[0]["id"]
        except IndexError as err:
            raise NoSuchArtist(f"No artist found with name {artist_name}") from err

    @staticmethod
    def _look_up_song_names(artist_id: str) -> Set[str]:
        """Look up names of songs by an artist."""
        limit = 100
        offset = 0
        release_list = []
        page = 1
        songs = set()

        page_releases = mbz.browse_releases(artist=artist_id, release_type=["album"], limit=limit)[
            "release-list"
        ]
        release_list += page_releases
        while len(page_releases) >= limit:
            offset += limit
            page += 1
            result = mbz.browse_releases(artist=artist_id,release_type=["album"], limit=limit, offset=offset)
            page_releases = result['release-list']
            release_list += page_releases

        for release in release_list:
            release_id = release["id"]
            release_track_list = mbz.get_release_by_id(
                release_id, includes=["recordings"]
            )
            tracks = release_track_list["release"]["medium-list"][0]["track-list"]
            for track in tracks:
                song_name = track["recording"]["title"]
                songs.add(song_name)

        return songs

    def look_up_artist(self, artist_name: str) -> Artist:
        """Look up an artist, returning the first match."""
        artist_id = self._look_up_artist_id(artist_name)
        song_names = self._look_up_song_names(artist_id)
        return Artist(artist_name, list(song_names))


class OVHLyricsAPI:
    """An API to look up song lyrics by an artist."""

    @staticmethod
    def _build_lyrics_url(artist_name: str, song_name: str) -> str:
        """Build a request URL to get the song lyrics."""
        lyrics_api_base = "https://api.lyrics.ovh/v1"
        lyrics_api_url = html.escape(f"{lyrics_api_base}/{artist_name}/{song_name}")
        return lyrics_api_url

    def request_song(self, artist_name: str, song_name: str) -> Optional[Song]:
        """Request an individual song by an artist."""
        url = self._build_lyrics_url(artist_name, song_name)
        try:
            response = requests.get(url)
        except requests.exceptions.HTTPError:
            return None

        try:
            lyric_string: str = response.json()["lyrics"]
        except (KeyError, ValueError):  # No lyrics for song in response.
            return None

        if not lyric_string:
            return None

        lyrics = lyric_string.translate(
            str.maketrans("", "", string.punctuation)
        ).split()
        if not lyrics:
            return None

        return Song(artist_name, song_name, lyrics)

    def request_songs(self, artist: Artist) -> Iterator[Song]:
        """
        Iterate through the artist's songs, yielding songs
        with complete lyrics.

        """
        for song_name in artist.song_names:
            song = self.request_song(artist.artist_name, song_name)
            if song is not None:
                yield song
