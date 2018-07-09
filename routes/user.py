import time
from aiohttp.web import json_response
from aiohttp_session import get_session
import sqlalchemy as sa
from model import sa_user, sa_group, sa_user_group


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
    data = await request.json()
    async with request.app.db.acquire() as conn:
        query = sa.select([sa_user, sa_user_group.c.user_id, sa_user_group.c.group_id, sa_group.c.role, sa_group.c.id.label('group_id_d')]) \
            .select_from(
            sa_user
                .join(sa_user_group, sa_user.c.id == sa_user_group.c.user_id, isouter=True)
                .join(sa_group, sa_user_group.c.group_id == sa_group.c.id, isouter=True)
        )

        print(query)
        users = list(
            map(lambda x: dict(x),
                await conn.execute(query)
                )
        )
    return json_response({"users": users})
