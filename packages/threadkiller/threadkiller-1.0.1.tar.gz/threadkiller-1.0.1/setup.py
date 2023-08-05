# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['threadkiller']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.5,<14.0']

setup_kwargs = {
    'name': 'threadkiller',
    'version': '1.0.1',
    'description': 'A Telegram bot to delete messages sent outside of channel comment threads',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
