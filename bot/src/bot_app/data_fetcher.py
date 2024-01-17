import os

import aiohttp

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

async def get_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(os.getenv('SENTENCES_API_URL_RANDOM')) as response:
            return await response.json()
