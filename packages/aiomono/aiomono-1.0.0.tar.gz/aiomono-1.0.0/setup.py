# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiomono']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aiomono',
    'version': '1.0.0',
    'description': 'The asynchronous library for monobank API',
    'long_description': None,
    'author': 'Artur',
    'author_email': 'arturboyun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
