# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_sdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'target-sdk',
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
