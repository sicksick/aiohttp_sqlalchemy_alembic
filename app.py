import pathlib
from aiohttp import web
from config import setup_config
from config.connect_redis import redis_connect
from db import init_pg, close_pg
from aiohttp_session import setup
from middleware.errors import errors_middleware
from middleware.police import police_middleware
from routes import apply_routes


async def dispose_redis_pool(app):
    redis_pool.close()
    await redis_pool.wait_closed()

app = web.Application()
# Add config to app
setup_config(app, pathlib.Path(__file__).parent)

# Redis connect
storage, redis_pool = redis_connect(app)
setup(app, storage)

# Add routes
apply_routes(app)

app.middlewares.append(police_middleware)
app.middlewares.append(errors_middleware)

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.on_cleanup.append(dispose_redis_pool)

web.run_app(app)
