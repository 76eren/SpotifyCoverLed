from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Artist:
    name: str
    id: str
    uri: str
    external_url: str

@dataclass
class Album:
    name: str
    id: str
    uri: str
    external_url: str
    release_date: str
    images: List[Dict[str, str]]

@dataclass
class Track:
    name: str
    id: str
    uri: str
    external_url: str
    artists: List[Artist]
    album: Album
    duration_ms: int
    is_explicit: bool
    popularity: int
    progress_ms: int
    is_playing: bool