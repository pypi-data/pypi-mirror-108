from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Genre:
    id: int
    name: str
    picture: str

    @staticmethod
    def from_dict(d: dict) -> Genre:
        return Genre(d["id"], d["name"], d["picture"])
