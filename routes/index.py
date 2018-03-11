import time
from aiohttp import web
from aiohttp_session import get_session


def init(app):
    prefix = '/api'
    app.router.add_get(prefix + '/as', home)
    app.router.add_get(prefix + '/', home)
    app.router.add_get(prefix + '/{name}', home)


async def home(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    text = 'Last visited: {}'.format(last_visit)
    return web.Response(text=text)



