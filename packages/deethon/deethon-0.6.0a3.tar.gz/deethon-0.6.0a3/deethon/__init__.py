"""
🎵 Deethon is a Python3 library to easily download music from Deezer and a
wrapper for the Deezer API with some extra features. 🎵
"""
from importlib import metadata

__version__ = metadata.version(__name__)

from . import errors, models
from .client import Client
from .models import Quality

__all__ = ["Client", "models", "Quality", "errors"]
