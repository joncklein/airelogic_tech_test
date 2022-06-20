from typing import List
from dataclasses import dataclass

from song import Song
 
@dataclass
class Artist:
 
    artist_name: str
    artist_id: str
    full_tracklist: List[Song]


