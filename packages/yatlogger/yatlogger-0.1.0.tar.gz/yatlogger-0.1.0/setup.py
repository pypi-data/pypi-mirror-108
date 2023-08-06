# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yatlogger']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.6,<14.0']

setup_kwargs = {
    'name': 'yatlogger',
    'version': '0.1.0',
    'description': 'Yet another telegram logger',
    'long_description': None,
    'author': 'cyd3r',
    'author_email': 'cyd3rhacker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
