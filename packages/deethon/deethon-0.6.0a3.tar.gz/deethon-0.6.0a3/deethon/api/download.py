from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, Callable, Union

from ..errors import DownloadError, InvalidUrlError, ActionNotSupported
from ..models import Quality, Track, Album
from ..utils import get_file_path, tag_flac, tag_id3
from ..utils.consts import DEEZER_ALBUM_REGEX, DEEZER_TRACK_REGEX

if TYPE_CHECKING:
    from .. import Client


async def download_track(
    self: Client,
    track: Union[str, int, Track],
    quality: Quality = Quality.FLAC,
    progress_callback: Callable[[int, int], None] = None,
    album: Album = None,
    cover: bytes = None
) -> Path:

    if isinstance(track, str):
        match = DEEZER_TRACK_REGEX.match(track)
        if match:
            track_id = int(match.group(1))
            track = await self.get_track(track_id)
        else:
            raise InvalidUrlError(track)

    elif not isinstance(track, Track):
        track = await self.get_track(track)

    if not album:
        album = await self.get_album(track.album.id)

    download_url = track.get_stream_url(quality)
    file_path = get_file_path(track, quality.get_file_ext())
    response = await self._req.get(download_url)
    total = response.content_length
    current = 0

    if not total:
        fallback_bitrate = quality.get_fallback_quality()
        if fallback_bitrate is None:
            raise DownloadError(track.id)
        return await self.download_track(track, fallback_bitrate, progress_callback)

    with file_path.open("wb") as f:
        async for data, _ in response.content.iter_chunks():
            current += len(data)
            f.write(data)
            if progress_callback:
                progress_callback(current, total)

    if not cover:
        cover = await album.download_cover(1200, 95)

    if quality == Quality.FLAC:
        tag_flac(file_path, track, album, cover)
    else:
        tag_id3(file_path, track, album, cover)

    return file_path.absolute()


async def download_album(self: Client, album: Union[str, int, Album], quality: Quality):
    """
    Downloads an album from Deezer using the specified Album object.

    Args:
        album: An [Album][deethon.models.Album] object or album id or Deezer album link.
        quality: The preferred quality to download.

    Returns:
        The file paths.
    """
    if isinstance(album, str):
        match = DEEZER_ALBUM_REGEX.match(album)
        if match:
            track_id = int(match.group(1))
            track = await self.get_track(track_id)
        else:
            raise InvalidUrlError(album)

    elif isinstance(album, int):
        album = await self.get_album(album)

    cover = await album.download_cover(1200, 95)

    for track in album.tracks:
        yield await self.download_track(track.id, quality, album=album, cover=cover)
