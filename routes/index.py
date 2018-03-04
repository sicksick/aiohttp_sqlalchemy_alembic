import time
from aiohttp import web
from aiohttp_session import get_session


def init(app):
    app.router.add_get('/', home)
    app.router.add_get('/{name}', home)


async def home(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    text = 'Last visited: {}'.format(last_visit)
    return web.Response(text=text)



