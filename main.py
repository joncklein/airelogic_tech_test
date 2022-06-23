from argparse import ArgumentParser
from statistics import mean
from typing import Iterator

from api import MusicBrainzArtistAPI, OVHLyricsAPI
from song import Song


VERSION = "0.1"
APP_NAME = "MU$IC F1NDER"
AUTHOR = "joncklein@gmail.com"


def calculate_average_words(songs: Iterator[Song]) -> float:
    """Calculate the mean number of words in an artist's songs."""
    return mean(map(len, songs))


def main() -> None:
    parser = ArgumentParser(
        prog=f"----++++{APP_NAME}++++----_",
        description="Find the average word count for any music artist.",
    )
    parser.add_argument("artist", type=str, help="the artist you wish to search for")
    args = parser.parse_args()

    artist_api = MusicBrainzArtistAPI(APP_NAME, VERSION, AUTHOR)
    artist = artist_api.look_up_artist(args.artist)

    song_api = OVHLyricsAPI()
    songs = song_api.request_songs(artist)
    average_count = calculate_average_words(songs)
    print(f"The average count of {artist.artist_name}'s songs is {average_count:,.2f}")


if __name__ == "__main__":
    main()
