from __future__ import annotations

from enum import Enum
from typing import Optional


class Quality(Enum):
    FLAC = "9"
    MP3_320 = "3"
    MP3_256 = "5"
    MP3_128 = "1"

    def get_file_ext(self) -> str:
        if self.value == "9":
            return "flac"
        return "mp3"

    def get_fallback_quality(self) -> Optional[Quality]:
        if self == Quality.FLAC:
            return Quality.MP3_320
        if self == Quality.MP3_320:
            return Quality.MP3_256
        if self == Quality.MP3_256:
            return Quality.MP3_128
        return None
