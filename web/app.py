import logging
import pathlib
import os
from aiohttp import web
from web.config import setup_config
from web.config.connect_redis import redis_connect
from web.config.db import init_pg, close_pg
from aiohttp_session import setup
from web.helpers.log import create_loggers
from web.middleware.errors import errors_middleware
from web.middleware.police import police_middleware
from web.routes import apply_routes


async def dispose_redis_pool(app):
    redis_pool.close()
    await redis_pool.wait_closed()

app = web.Application()
# Add config to app
setup_config(app, pathlib.Path(__file__).parent)

if os.getenv('DEBUG', False) is True:
    logging.getLogger().setLevel(logging.INFO)
    logging.debug("Logging started")


# Redis connect
storage, redis_pool = redis_connect(app)
setup(app, storage)

# Create log
create_loggers(app)

# Add routes
apply_routes(app)

#  before
app.middlewares.append(police_middleware)

#  after
app.middlewares.append(errors_middleware)

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.on_cleanup.append(dispose_redis_pool)

web.run_app(app, host=os.getenv('HOST', '0.0.0.0'), port=os.getenv('PORT', '8000'))
