"""
The utils module contains several useful functions that are used within the package.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Track


def get_file_path(track: Track, ext: str) -> Path:
    """
    Generate a file path using a Track object.

    Args:
        track: A Track object.
        ext: The file extension to be used.

    Returns:
        A Path object containing the track path.
    """
    forbidden_chars = dict((ord(char), None) for char in r'\/*?:"<>|')
    album_artist = track.artist.name.translate(forbidden_chars)
    album_title = track.album.title.translate(forbidden_chars)

    std_dir = "Songs"
    dir_path = Path(std_dir, album_artist, album_title)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{track.track_position:02} {track.title}.{ext}"
    return dir_path / file_name.translate(forbidden_chars)
