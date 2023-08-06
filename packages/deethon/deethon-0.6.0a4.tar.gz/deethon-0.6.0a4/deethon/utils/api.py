from binascii import b2a_hex
from hashlib import md5

from Crypto.Cipher import AES

from .. import Quality
from ..errors import DeezerApiError


def raise_if_error(body: dict):
    if "error" in body:
        error = body["error"]
        raise DeezerApiError(
            error["type"],
            error["message"],
            error["code"]
        )


def get_stream_url(track_id: int, md5_origin: str, media_version: int, quality: Quality) -> str:
    data = b"\xa4".join(
        a.encode() for a in [md5_origin, quality.value,
                             str(track_id), str(media_version)]
    )
    data = b"\xa4".join(
        [md5(data).hexdigest().encode(), data]) + b"\xa4"
    if len(data) % 16:
        data += b"\x00" * (16 - len(data) % 16)
    c = AES.new(b"jo6aey6haid2Teih", AES.MODE_ECB)
    hashs = b2a_hex(c.encrypt(data)).decode()
    return f"http://e-cdn-proxy-{self.md5_origin[0]}.dzcdn.net/api/1/{hashs}"
