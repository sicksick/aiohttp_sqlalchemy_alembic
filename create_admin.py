import asyncio
import os
import aiopg.sa
import bcrypt
from sqlalchemy import text
from app import app
from models.user import sa_user
from models.user_group import sa_user_group


async def create_admin():
    email = 'admin@example.com'
    password = 'qwerqwer'

    engine = await aiopg.sa.create_engine(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        minsize=1,
        maxsize=5,
        loop=app.loop)
    data = {
        'email': email,
        'name': 'admin',
        'image': '/media/avatars/default.png',
        'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'roles': ['admin']
    }
    roles = data['roles']
    del data['roles']
    async with engine.acquire() as conn:
        query = sa_user.insert().values(data)
        user = list(map(lambda x: dict(x), await conn.execute(query)))
        new_user_id = user[0]['id']

        for role in roles:
            query = text("""
                            SELECT
                                roles.*
                            FROM roles
                            where
                                roles.name = :role_name
                            ;
                        """)
            query_result = await conn.execute(query, role_name=role)
            found_role = await query_result.fetchone()
            query = sa_user_group.insert().values({'user_id': new_user_id, 'role_id': dict(found_role)['id']})
            await conn.execute(query)
    return new_user_id


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_admin())
    loop.close()
