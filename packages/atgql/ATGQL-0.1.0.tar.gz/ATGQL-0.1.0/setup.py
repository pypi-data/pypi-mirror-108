# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atgql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'atgql',
    'version': '0.1.0',
    'description': 'A Python port of graphql-js and dataloader',
    'long_description': '',
    'author': 'iyanging',
    'author_email': 'iyanging@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
