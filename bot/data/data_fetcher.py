import aiohttp

# убрать эту переменную в .env
SENTENCES_API_URL_RANDOM = "http://127.0.0.1:8000/random"


async def get_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(SENTENCES_API_URL_RANDOM) as response:
            return await response.json()
