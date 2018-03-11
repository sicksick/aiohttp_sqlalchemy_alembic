import aiopg.sa


async def init_pg(app):
    conf = app.config['connection']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    setattr(app, 'db', engine)


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

