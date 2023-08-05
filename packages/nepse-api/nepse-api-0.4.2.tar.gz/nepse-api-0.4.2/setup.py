# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nepse', 'nepse.security']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.2,<5.0.0', 'httpx>=0.18.1,<0.19.0', 'pyhumps>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'nepse-api',
    'version': '0.4.2',
    'description': 'This is a API wrapper for NEPSE API.',
    'long_description': None,
    'author': 'Samrid Pandit',
    'author_email': 'samrid.pandit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
