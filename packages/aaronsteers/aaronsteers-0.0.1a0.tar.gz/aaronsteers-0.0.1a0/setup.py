# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aaronsteers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aaronsteers',
    'version': '0.0.1a0',
    'description': "It's me, AJ! Hi.",
    'long_description': None,
    'author': 'AJ Steers',
    'author_email': 'aaronsteers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
