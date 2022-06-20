from argparse import ArgumentParser
from statistics import mean

from artist import Artist
from api import RealArtistAPI
from api import RealLyricsAPI


def calculate_average_words(artist: Artist, song_api: RealLyricsAPI) -> float:
    """Calculate the mean number of words in an artist's songs."""
    return mean(map(len, artist.get_songs(song_api)))

def main() -> None:

	parser = ArgumentParser(
		prog="----++++MU$IC F1NDER++++----", description="Find the average word count for any music artist."
	)
	parser.add_argument(
		"--artist", "-a", type=str, help="the artist you wish to search for"
	)
	parser.add_argument(
		"--useragent", "-u", type=list, default=['testagent', '0.1'], help='useragent to use for musicbrainz'
	)

	args = parser.parse_args()
	

if __name__ == "__main__":
    main()