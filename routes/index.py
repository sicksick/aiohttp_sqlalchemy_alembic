import time

import aiohttp_jinja2
from aiohttp_session import get_session


def init(app):
    app.router.add_get('/', home)


@aiohttp_jinja2.template('index.html')
async def home(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    text = 'Last visited: {}'.format(last_visit)
    return {'text': text}



