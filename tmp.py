

import aiohttp

async def a():
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            "http://172.16.12.19/ntls/license.json"
        )
        x = await resp.text()
        print(x)
        return resp
    

import asyncio

asyncio.run(a())