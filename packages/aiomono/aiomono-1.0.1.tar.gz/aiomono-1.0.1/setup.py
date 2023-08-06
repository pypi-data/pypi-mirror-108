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
    'version': '1.0.1',
    'description': 'The asynchronous library for monobank API',
    'long_description': "# AIOMono (Alpha)\n\nThe **aiomono** is fully asynchronous library for [Monobank API](https://api.monobank.ua/docs) written in Python 3.7 with [asyncio](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://github.com/aio-libs/aiohttp) and [pydantic](https://pydantic-docs.helpmanual.io/).\n\n\n## Setup\n- You get token for your client from [MonobankAPI](https://api.monobank.ua/).\n- Install the **latest version** of the **aiomono**: `pip install aiomono`\n\n## Examples\n\n**We have 3 different classes for use Monobank API:**\n- `MonoClient` is simple base class for others, can only get currencies\n- `PersonalMonoClient` - this class for talk to personal Monobank API\n- ~~`CorporateMonoClient` - this class for talk to corporate Monobank API~~ (not realized)\n\n\n### Simple [get_currency](https://api.monobank.ua/docs/#operation--bank-currency-get) request\n\n```python\nimport asyncio\nfrom aiomono import MonoClient\n\nmono_client = MonoClient()\n\nasync def main():\n    async with mono_client as client:\n        client_info = await client.get_currency()\n        print(client_info)\n\nasyncio.run(main())\n```\n\n### [client_info](https://api.monobank.ua/docs/#operation--personal-client-info-get) request\n\n```python\nimport asyncio\nfrom aiomono import PersonalMonoClient\n\nMONOBANK_API_TOKEN = 'uXZquoEm6P4aGVnJeJjVrujvbKmd_GHXxF5LEgcsM8mE'\n\n\nasync def main():\n    try:\n        mono_client = PersonalMonoClient(MONOBANK_API_TOKEN)\n        client_info = await mono_client.client_info()\n        print(f'User {client_info.name} syccessfuly authorized😍')\n    finally:\n        await mono_client.close()\n\nasyncio.run(main())\n```\n\n### Resources:\n`# TODO`\n",
    'author': 'Archie',
    'author_email': 'arturboyun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/archiesir/aiomono',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
