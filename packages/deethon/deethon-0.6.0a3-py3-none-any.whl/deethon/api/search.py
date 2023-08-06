from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import SearchTrack, SearchAlbum
from ..utils import raise_if_error

if TYPE_CHECKING:
    from .. import Client


async def search_track(self: Client, term: str) -> list[SearchTrack]:
    token = await self.session.token()
    url = f"http://api.deezer.com/search/track?q={term}&access_token={token}"
    res = await self._req.get(url)
    body = await res.json()
    raise_if_error(body)
    results = list(map(lambda x: SearchTrack.from_dict(x), body["data"]))
    return results


async def search_album(self: Client, term: str) -> list[SearchAlbum]:
    token = await self.session.token()
    url = f"http://api.deezer.com/search/album?q={term}&access_token={token}"
    res = await self._req.get(url)
    body = await res.json()
    raise_if_error(body)
    results = list(map(lambda x: SearchAlbum.from_dict(x), body["data"]))
    return results
