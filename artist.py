from typing import List
from dataclasses import dataclass


@dataclass
class Artist:
    """A musical artist."""

    artist_name: str
    """The name of the artist."""
    song_names: List[str]
    """A full list of the artist's current song titles."""
