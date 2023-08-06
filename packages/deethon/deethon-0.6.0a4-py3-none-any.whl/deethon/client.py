import aiohttp

from .session import Session


class Client:
    def __init__(self, proxy: str = None) -> None:
        self._req = aiohttp.ClientSession(trust_env=True)
        self.session = Session(self)

    from .api.api import get_track, get_album
    from .api.download import download_track, download_album
    from .api.search import search_track, search_album

    async def close(self):
        await self._req.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._req.close()
