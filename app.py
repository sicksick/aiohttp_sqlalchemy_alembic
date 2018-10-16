import logging
import os
import socketio
from config.jinja_init import jinja_init
from aiohttp import web
from config import setup_config
from config.connect_redis import redis_connect
from config.db import init_pg, close_pg
from aiohttp_session import setup
from helpers.log import create_loggers
from socket_io.main import get_socket_io_route
from middleware.errors import errors_middleware
from middleware.police import police_middleware
from routes import apply_routes
from aiojobs.aiohttp import setup as setup_aiojobs


async def dispose_redis_pool(app):
    redis_pool.close()
    await redis_pool.wait_closed()


sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

# Add config to app
setup_config(app)

# Add templates render
jinja_init(app)

if bool(os.getenv('DEBUG', False)) is True:
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

sio, background_task = get_socket_io_route(sio, app)

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.on_cleanup.append(dispose_redis_pool)
sio.start_background_task(background_task)
setup_aiojobs(app)

if __name__ == '__main__':
    web.run_app(app, host=os.getenv('HOST', '0.0.0.0'), port=os.getenv('PORT', '8080'))
