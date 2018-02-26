from aiohttp import web
from db import init_pg, close_pg
import yaml


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    data = {'some': 'data'}
    return web.json_response(data)
    # return web.Response(text=text)


app = web.Application()

with open("config.yaml", 'r') as stream:
    try:
        app['config'] = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app)
