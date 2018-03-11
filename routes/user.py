import time
from aiohttp.web import json_response, HTTPServerError
from aiohttp_session import get_session
from model import sa_user


def init(app):
    prefix = ''
    app.router.add_post(prefix + '/login', login)
    app.router.add_post(prefix + '/registration', registration)

    prefix = '/api/user'
    app.router.add_get(prefix + '/{id}', login)
    app.router.add_put(prefix + '/{id}', login)


async def login(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()
    text = 'Last visited: {}'.format(last_visit)
    return json_response({"ssss": "asdasd"})


async def registration(request):
    try:
        data = await request.json()
        async with request.app.db.acquire() as conn:
            users = list(map(lambda x: dict(x), await conn.execute(sa_user
                                                                   .select()
                                                                   .where(sa_user.c.id == 1)
                                                                   )))
            users
        return json_response({"users": users})
    except Exception as e:
        return HTTPServerError()



