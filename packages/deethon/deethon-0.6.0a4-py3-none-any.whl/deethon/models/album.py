from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from .genre import Genre
from .track import TrackArtist

if TYPE_CHECKING:
    from .. import Client


@dataclass
class AlbumTrack:
    """
    The Track class contains several information about a track.

    Attributes:
        artist: The main artist of the track.
        duration: The duration of the track.
        id: The Deezer ID of the track.
        link: The Deezer link of the track.
        preview_link: The link to a 30 second preview of the track.
        rank: The rank of the track on Deezer
        lyrics_id: The lyrics of the track.
        md5_origin: The md5 origin of the track.
        media_version: The media version of the track.
        title: The title of the track.
        title_short: The short title of the track.
    """
    artist: TrackArtist
    duration: int
    id: int
    link: str
    preview_link: str
    rank: int
    lyrics_id: int
    md5_image: str
    md5_origin: str
    media_version: int
    title: str
    title_short: str

    @staticmethod
    def from_dict(d: dict) -> AlbumTrack:
        return AlbumTrack(
            artist=TrackArtist.from_dict(d["artist"]),
            duration=d["duration"],
            id=d["id"],
            link=d["link"],
            preview_link=d["preview"],
            rank=d["rank"],
            lyrics_id=d["lyrics_id"],
            md5_image=d["md5_image"],
            md5_origin=d["md5_origin"],
            media_version=d["media_version"],
            title=d["title"],
            title_short=d["title_short"],
        )


@dataclass
class Album:
    """
    The Album class contains several information about an album.

    Attributes:
        artist: The main artist of the album.
        duration: The duration in seconds of the album.
        genres: A list of genres of the album.
        id: The Deezer ID of the album.
        label: The label of the album.
        link: The Deezer link of the album.
        nb_tracks: The total number of tracks in the album.
        record_type: The record type of the album.
        release_date: The release date of the album.
        title: The title of the album.
        tracks: A list that contains basic tracks data.
        upc: The Universal Product Code (UPC) of the album.

    """
    artist: TrackArtist
    duration: int
    genres: list[Genre]
    id: int
    label: str
    link: str
    md5_image: str
    nb_tracks: int
    record_type: str
    release_date: datetime
    title: str
    tracks: list[AlbumTrack]
    upc: str
    _client: Client

    @staticmethod
    def from_dict(client: Client, d: dict) -> Album:
        return Album(
            artist=TrackArtist.from_dict(d["artist"]),
            duration=d["duration"],
            genres=[Genre.from_dict(x) for x in d["genres"]["data"]],
            id=d["id"],
            label=d["label"],
            link=d["link"],
            md5_image=d["md5_image"],
            record_type=d["record_type"],
            release_date=datetime.strptime(d["release_date"], "%Y-%m-%d"),
            title=d["title"],
            tracks=[AlbumTrack.from_dict(x)
                    for x in d["tracks"]["data"]],
            nb_tracks=d["nb_tracks"],
            upc=d["upc"],
            _client=client
        )

    def get_cover_url(self, size: int = 250, quality: int = 80) -> str:
        """
        Get the URL of the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        return f"http://cdn-images.dzcdn.net/images/cover/{self.md5_image}/{size}x{size}-000000-{quality}-0-0.jpg"

    async def download_cover(self, size: int = 250, quality: int = 80) -> bytes:
        """
        Downloads the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        cover_url = self.get_cover_url(size, quality)
        response = await self._client._req.get(cover_url)
        return await response.read()


@dataclass
class SearchAlbum:
    artist: TrackArtist
    id: int
    md5_image: str
    title: str
    genre_id: int
    record_type: str
    link: str
    nb_tracks: int

    @staticmethod
    def from_dict(d: dict) -> SearchAlbum:
        return SearchAlbum(
            artist=TrackArtist(d["artist"]["id"], d["artist"]["name"]),
            id=d["id"],
            md5_image=d["md5_image"],
            genre_id=d["genre_id"],
            link=d["link"],
            title=d["title"],
            record_type=d["record_type"],
            nb_tracks=d["nb_tracks"]
        )

    def get_cover_url(self, size: int = 250, quality: int = 80) -> str:
        """
        Get the URL of the album cover.

        Args:
            size: The size of the album cover in pixels (should not exceed 1200).
            quality: The quality of the album cover (should be between 0 and 100).
        """
        return f"http://cdn-images.dzcdn.net/images/cover/{self.md5_image}/{size}x{size}-000000-{quality}-0-0.jpg"
