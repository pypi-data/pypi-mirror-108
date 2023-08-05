# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['playlist_along', 'playlist_along.commands']

package_data = \
{'': ['*']}

install_requires = \
['charset-normalizer>=1.3.9,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'mutagen>=1.45.1,<2.0.0',
 'natsort>=7.1.1,<8.0.0',
 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['playlist-along = playlist_along.__main__:main']}

setup_kwargs = {
    'name': 'playlist-along',
    'version': '2021.6.1',
    'description': 'Python CLI app for M3U playlists conversion and processing',
    'long_description': 'Playlist Along\n==============\n\n|Status| |PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n|Black|\n\n.. |Status| image:: https://raster.shields.io/badge/Status-beta-26972D\n   :target: https://raster.shields.io/badge/Status-beta-26972D\n   :alt: Project Status\n.. |PyPI| image:: https://img.shields.io/pypi/v/playlist-along.svg\n   :target: https://pypi.org/project/playlist-along/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/playlist-along\n   :target: https://pypi.org/project/playlist-along\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/playlist-along.svg\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/playlist-along/latest.svg?label=Read%20the%20Docs\n   :target: https://playlist-along.readthedocs.io/\n   :alt: Read the documentation at https://playlist-along.readthedocs.io/\n.. |Tests| image:: https://github.com/hotenov/playlist-along/workflows/Tests/badge.svg\n   :target: https://github.com/hotenov/playlist-along/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/hotenov/playlist-along/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/hotenov/playlist-along\n   :alt: Codecov\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n🧐 About\n---------\n\nHave you ever wanted to take your favorite offline playlist along?\n— *I have.*\n\nThis script makes it easier to do that.\nIt converts your playlist with absolute paths\nto playlist with relative paths,\nand copies audio files to one folder with converted playlist.\nThe only thing that remains to be done is to move this folder\nto your Android smartphone and open the playlist\n(or let a player to discover media for you).\n\nAlthough, there is only one conversion way\n"Desktop `AIMP`_ -> `VLC for Android`_" for now, \nbut who knows what the future holds for us?\n\n🚀 Features\n------------\n\n*  Conversion from **AIMP** *(desktop)* .m3u / .m3u8 playlists\n   into playlists suitable for playback in **VLC for Android**\n   (with relative paths,\n   replaced square brackets ``[`` ``]`` and *hash* ``#`` \n   in songs filenames)\n*  Copying songs from .m3u / .m3u8 playlists into destination folder\n   (after playlist conversion and only **.mp3** and **.flac** local files, for now)\n*  Displaying only tracks from playlist\n   *(without M3U tag lines / comments)*\n*  Displaying a full content of playlist file\n*  Creating a playlist from tracks of specified folder\n   (with relative or absolute paths)\n*  Injecting (appending) one playlist into another \n   (top or bottom)\n*  Creating an empty playlist file\n*  **TBD:** Copying and conversion paths to relative, without replacing characters\n   ("make relative playlist")\n\n🛠️ Requirements\n----------------\n\n* Python 3.6.2 and higher\n\nInstalling Python is no different than installing other apps for your OS.\nGo to downloads page on `python.org <https://www.python.org/downloads/>`_.\nDownload the latest version for your OS or any version higher than ``3.6.2``.\nThen run Python installer and follow its steps.\n\n\n💻 Installation\n----------------\n\nYou can install *Playlist Along* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install playlist-along\n\nI do recommend you to use `pipx`_ for any CLI Python package.\nIt let you install and run Python applications in isolated environments.\n\n.. code:: console\n\n   $ python -m pip install --user pipx\n   $ pipx install playlist-along\n   $ playlist-along --version\n\n🕹 Usage\n--------\n\nPlease see the `Usage Examples <Usage_>`_ or the `Command-line Reference <Manpage_>`_ for details.\n\n\n✊ Contributing\n---------------\n\nIf you want to suggest a new feature or to ask questions about this project,\nyou can open a `new discussion`_.\n\nWant to implement or fix something? - contributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\n📝 License\n-----------\n\nDistributed under the terms of the `MIT license`_,\n*Playlist Along* is free and open source software.\n\n\n🐞 Issues\n----------\n\nIf you encounter any problems,\nplease see `project discussions`_ first \nor `file an issue`_ along with a detailed description.\n\n\n🙏🏻 Credits\n------------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\nScript uses the following packages / libraries under the hood:\n\n* `Click`_, of course (`BSD-3-Clause License <https://github.com/pallets/click/blob/main/LICENSE.rst>`_)\n* `charset_normalizer <https://github.com/Ousret/charset_normalizer>`_, for auto encoding detecting of playlist files (MIT License)\n* `single-source <https://github.com/rabbit72/single-source>`_, for getting project version from anywhere (MIT License)\n* `natsort <https://github.com/SethMMorton/natsort>`_, to get tracks order as you see in File Explorer (MIT License)\n* `mutagen <https://github.com/quodlibet/mutagen>`_, to handle audio metadata (GPL-2.0 License)\n\nand other amazing Python packages for development and testing.\n\nSee a full list of dev dependencies in ``pyproject.toml``\n`here <https://github.com/hotenov/playlist-along/blob/main/pyproject.toml#L29>`_.\n\n\n.. _AIMP: https://www.aimp.ru/\n.. _VLC for Android: https://play.google.com/store/apps/details?id=org.videolan.vlc&hl=en&gl=US\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/project/playlist-along/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/hotenov/playlist-along/issues\n.. _pip: https://pip.pypa.io/\n.. _new discussion: https://github.com/hotenov/playlist-along/discussions/new\n.. _project discussions: https://github.com/hotenov/playlist-along/discussions\n.. _Click: https://github.com/pallets/click\n.. _pipx: https://pipxproject.github.io/pipx/\n\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://playlist-along.readthedocs.io/en/latest/usage.html\n.. _Manpage: https://playlist-along.readthedocs.io/en/latest/manpage.html\n',
    'author': 'Artem Hotenov',
    'author_email': 'qa@hotenov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotenov/playlist-along',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
