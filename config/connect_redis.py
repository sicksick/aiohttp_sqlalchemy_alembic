import aioredis
import asyncio

import os
from aiohttp_session.redis_storage import RedisStorage


def redis_connect(app):
    async def make_redis_pool():
        redis_address = (os.getenv('REDIS_HOST', 'redis'), os.getenv('REDIS_PORT', '6379'))
        return await aioredis.create_redis_pool(redis_address, timeout=1)

    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(redis_pool)
    return storage, redis_pool

