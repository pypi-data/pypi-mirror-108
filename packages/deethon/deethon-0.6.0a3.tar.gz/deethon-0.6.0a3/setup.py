# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deethon', 'deethon.api', 'deethon.models', 'deethon.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'mutagen>=1.45.1,<2.0.0',
 'pycryptodome>=3.10.1,<4.0.0']

setup_kwargs = {
    'name': 'deethon',
    'version': '0.6.0a3',
    'description': 'Python3 library to easily download music from Deezer',
    'long_description': '# Deethon\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3a54b30586b941acb82079d0252e0320)](https://www.codacy.com/gh/deethon/deethon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=deethon/deethon&amp;utm_campaign=Badge_Coverage)\n[![PyPI](https://img.shields.io/pypi/v/deethon)](https://pypi.org/project/deethon/)\n[![PyPI - Downloads](https://pepy.tech/badge/deethon)](https://pepy.tech/project/deethon)\n![PyPI - Status](https://img.shields.io/pypi/status/deethon)\n[![GitHub license](https://img.shields.io/github/license/aykxt/deethon)](https://github.com/aykxt/deethon/blob/master/LICENSE)\n\nDeethon is a lightweight Python library for downloading high quality music from Deezer.\n\n## Getting started\n\n### Installation\n\n```sh\npip install deethon\n```\n\n### Usage\n\n```python\nfrom deethon import Session, Quality\n\ndeezer = Session("YOUR ARL TOKEN")\n\ndeezer.download_track(\n    "https://www.deezer.com/track/1234567",\n    Quality.MP3_320  # defaults to FLAC\n)\n```\n',
    'author': 'Aykut Yilmaz',
    'author_email': 'aykuxt@gmail.com',
    'maintainer': 'Aykut Yilmaz',
    'maintainer_email': 'aykuxt@gmail.com',
    'url': 'https://github.com/aykxt/deethon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
