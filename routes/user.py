import time
from aiohttp.web import json_response
from aiohttp_session import get_session
import sqlalchemy as sa
from model import sa_user, sa_group, sa_user_group


def init(app):
    prefix = '/api'
    app.router.add_post(prefix + '/login', login)
    # app.router.add_post(prefix + '/registration', registration)
    #
    # prefix = '/api/user'
    # app.router.add_get(prefix + '/{id}', login)
    # app.router.add_put(prefix + '/{id}', login)


async def login(request):
    data = await request.json()
    async with request.app.db.acquire() as conn:
        users = list(map(lambda x: dict(x),
            await conn.execute("""
SELECT 
  users.id,
  users.email, 
  users.password, 
  to_char(users.created_at, 'DD-MM-YYYY HH24:MI:SS') as created_at, 
  to_char(users.updated_at, 'DD-MM-YYYY HH24:MI:SS') as updated_at
FROM users;
""")
            )
        )

    return json_response({"users": users})


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
