# Deethon

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Coverage)
[![PyPI](https://img.shields.io/pypi/v/deethon)](https://pypi.org/project/deethon/)
[![PyPI - Downloads](https://pepy.tech/badge/deethon)](https://pepy.tech/project/deethon)
![PyPI - Status](https://img.shields.io/pypi/status/deethon)
[![GitHub license](https://img.shields.io/github/license/aykxt/deethon)](https://github.com/aykxt/deethon/blob/master/LICENSE)

Deethon is a lightweight Python library for downloading high quality music from Deezer.

## Getting started

### Installation

```sh
pip install deethon
```

### Usage

```python
from deethon import Session, Quality

deezer = Session("YOUR ARL TOKEN")

deezer.download_track(
    "https://www.deezer.com/track/1234567",
    Quality.MP3_320  # defaults to FLAC
)
```
