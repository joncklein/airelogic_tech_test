from dataclasses import dataclass
from typing import List
 
@dataclass
class Song:
 
    song_name: str
    lyrics: List[str]
    word_count: int