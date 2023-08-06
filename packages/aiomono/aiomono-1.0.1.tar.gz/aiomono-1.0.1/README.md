# AIOMono (Alpha)

The **aiomono** is fully asynchronous library for [Monobank API](https://api.monobank.ua/docs) written in Python 3.7 with [asyncio](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://github.com/aio-libs/aiohttp) and [pydantic](https://pydantic-docs.helpmanual.io/).


## Setup
- You get token for your client from [MonobankAPI](https://api.monobank.ua/).
- Install the **latest version** of the **aiomono**: `pip install aiomono`

## Examples

**We have 3 different classes for use Monobank API:**
- `MonoClient` is simple base class for others, can only get currencies
- `PersonalMonoClient` - this class for talk to personal Monobank API
- ~~`CorporateMonoClient` - this class for talk to corporate Monobank API~~ (not realized)


### Simple [get_currency](https://api.monobank.ua/docs/#operation--bank-currency-get) request

```python
import asyncio
from aiomono import MonoClient

mono_client = MonoClient()

async def main():
    async with mono_client as client:
        client_info = await client.get_currency()
        print(client_info)

asyncio.run(main())
```

### [client_info](https://api.monobank.ua/docs/#operation--personal-client-info-get) request

```python
import asyncio
from aiomono import PersonalMonoClient

MONOBANK_API_TOKEN = 'uXZquoEm6P4aGVnJeJjVrujvbKmd_GHXxF5LEgcsM8mE'


async def main():
    try:
        mono_client = PersonalMonoClient(MONOBANK_API_TOKEN)
        client_info = await mono_client.client_info()
        print(f'User {client_info.name} syccessfuly authorized😍')
    finally:
        await mono_client.close()

asyncio.run(main())
```

### Resources:
`# TODO`
