import aioredis
import asyncio

from aiohttp_session.redis_storage import RedisStorage


def redis_connect(app):
    async def make_redis_pool():
        redis_address = (app.config['redis']['host'], app.config['redis']['port'])
        return await aioredis.create_redis_pool(redis_address, timeout=1)

    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(redis_pool)
    return storage, redis_pool

