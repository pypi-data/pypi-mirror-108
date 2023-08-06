from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, Frames

if TYPE_CHECKING:
    from ..models import Track, Album


def tag_id3(file_path: Path, track: Track, album: Album, picture: bytes) -> None:
    """
    Tag the music file at the given file path using the specified
    [Track][deethon.types.Track] instance.

    Args:
        file_path (Path): The music file to be tagged
        track: The [Track][deethon.types.Track] instance to be used for tagging.
    """
    tags = ID3()
    tags.clear()

    tags.add(Frames["TALB"](encoding=3, text=track.album.title))
    tags.add(Frames["TBPM"](encoding=3, text=str(track.bpm)))
    if album.genres:
        tags.add(Frames["TCON"](encoding=3, text=album.genres[0].name))
    # tags.add(Frames["TCOP"](encoding=3, text=track.copyright))
    tags.add(Frames["TDAT"](encoding=3,
                            text=track.release_date.strftime("%d%m")))
    tags.add(Frames["TIT2"](encoding=3, text=track.title))
    tags.add(Frames["TPE1"](encoding=3, text=track.artist.name))
    tags.add(Frames["TPE2"](encoding=3, text=album.artist.name))
    tags.add(Frames["TPOS"](encoding=3, text=str(track.disk_number)))
    tags.add(Frames["TPUB"](encoding=3, text=album.label))
    tags.add(Frames["TRCK"](encoding=3,
                            text=f"{track.track_position}/{album.nb_tracks}"))
    tags.add(Frames["TSRC"](encoding=3, text=track.isrc))
    tags.add(Frames["TYER"](encoding=3, text=str(track.release_date.year)))

    tags.add(Frames["TXXX"](encoding=3,
                            desc="replaygain_track_gain",
                            text=str(track.replaygain_track_gain)))

    # if track.lyrics:
    #     tags.add(Frames["USLT"](encoding=3,
    #                             text=track.lyrics))

    tags.add(Frames["APIC"](encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=picture))

    tags.save(file_path, v2_version=3)


def tag_flac(file_path, track: Track, album: Album, picture: bytes):
    tags = FLAC(file_path)
    tags.clear()
    tags["album"] = track.album.title
    tags["albumartist"] = album.artist.name
    tags["artist"] = track.artist.name
    tags["bpm"] = str(track.bpm)
    # tags["copyright"] = track.copyright
    tags["date"] = track.release_date.strftime("%Y-%m-%d")
    if album.genres:
        tags["genre"] = album.genres[0].name
    tags["isrc"] = track.isrc
    # if track.lyrics:
    #     tags["lyrics"] = track.lyrics
    tags["replaygain_track_gain"] = str(track.replaygain_track_gain)
    tags["title"] = track.title
    tags["tracknumber"] = str(track.track_position)
    tags["year"] = str(track.release_date.year)

    tags.clear_pictures()
    cover = Picture()
    cover.type = 3
    cover.data = picture
    cover.width = 1000
    cover.height = 1000
    tags.add_picture(cover)
    tags.save()
