# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['map_sdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'map-sdk',
    'version': '0.0.1a0',
    'description': 'SDK under development',
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aj@meltano.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
