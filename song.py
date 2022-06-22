from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    """A representation of a song."""

    artist_name: str
    song_name: str
    lyrics: List[str]

    @property
    def word_count(self):
        return len(self.lyrics)

    def __len__(self) -> int:
        return self.word_count
