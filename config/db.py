import os

import aiopg.sa

from config import config


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        minsize=1,
        maxsize=5,
        loop=app.loop)
    config['db'] = engine
    setattr(app, 'db', engine)


async def close_pg(app):
    app.db.close()
    await app.db.wait_closed()

