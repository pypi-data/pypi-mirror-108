from __future__ import annotations

from time import time
import asyncio
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


TOKEN_ENDPOINT = "http://connect.deezer.com/oauth/access_token.php?grant_type=client_credentials&client_id=447462&client_secret=a83bf7f38ad2f137e444727cfc3775cf&output=json"


class Session:
    def __init__(self, client: Client) -> None:
        self.client = client
        self._token = ""
        self._expires = 0.0
        self.lock = asyncio.Lock()

    async def fetch_token(self):
        res = await self.client._req.get(TOKEN_ENDPOINT)
        body = json.loads(await res.text())
        self._expires = time() + 3600  # 1 hour
        self._token = body["access_token"]

    async def token(self) -> str:
        async with self.lock:
            if self._expires < time():
                await self.fetch_token()
        return self._token
