# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbwrap']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0',
 'requests>=2.23,<3.0',
 'twine>=3.1,<4.0',
 'wheel>=0.34.2,<0.35.0']

setup_kwargs = {
    'name': 'pbwrap',
    'version': '1.3.1',
    'description': 'A Pastebin API Wrapper for Python',
    'long_description': '# Pastebin API wrapper for Python (pbwrap)\n[![PyPI version](https://badge.fury.io/py/pbwrap.svg)](https://badge.fury.io/py/pbwrap)\n[![Build Status](https://travis-ci.org/Mikts/pbwrap.svg?branch=master)](https://travis-ci.org/Mikts/pbwrap)\n[![Coverage Status](https://coveralls.io/repos/github/Mikts/pbwrap/badge.svg)](https://coveralls.io/github/Mikts/pbwrap)\n\n\n>**Python API wrapper for the Pastebin Public API.  \n**Only  _Python 3_ supported!**\n\n## Documentation\n\nThis wrapper is based on **Pastebin** API read their Documentation [**here.**](https://pastebin.com/api)  \nfor extra information and usage guide.\n\n### Usage\nFor a full list of the methods offered by the package [**Read.**](http://pbwrap.readthedocs.io/en/latest/)\n\n#### Quickstart\nImport and instantiate a Pastebin Object.\n```Python\nfrom pbwrap import Pastebin\n\npastebin = Pastebin(api_dev_key)\n```\n\n### Examples\n\n##### Get User Id\nReturns a string with the user_id created after authentication.\n```Python\nuser_id = pastebin.authenticate(username, password)\n```\n\n##### Get Trending Pastes details\nReturns a list containing Paste objects of the top 18 trending Pastes.\n\n```Python\ntrending_pastes = pastebin.get_trending()\n```\n\n### Type models\n\n#### Paste\n\nSome API endpoints return paste data in xml format the wrapper either converts them in a python dictionary format  \nor returns them as Paste objects which contain the following fields:\n\n* **key**\n* **date** in  **_UNIXTIME_**\n* **title**\n* **size**\n* **expire_date**\n* **private**\n* **format_short**\n* **format_long**\n* **url**\n* **hits**\n\n## License\npbwrap is released under [**MIT License**](./LICENSE)\n',
    'author': 'Mikts',
    'author_email': 'mikts94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mikts/pbwrap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
