import logging
import jwt
from config.config import config
from models.user import User
from socket_io.helper import get_and_send_participated_by_user_id, send_messages_by_chat_name
from socket_io.routes.chat import get_chat_routes
from socket_io.config import ROUTES, users_socket, users_by_user_id
from socket_io.routes.user import get_user_routes

logger = logging.getLogger('Rotating Log')


def get_socket_io_route(sio, app):

    get_user_routes(sio, app)

    get_chat_routes(sio, app)


    @sio.on(ROUTES['BACK']['CONNECT'])
    async def connect(sid, environ):
        token = environ.get('HTTP_AUTHORIZATION')

        try:
            decode = jwt.decode(token, config['secret'], algorithms=['HS256'])
        except jwt.DecodeError:
            return await sio.disconnect(sid)
        except Exception as e:
            return await sio.disconnect(sid)

        decode['user']['roles'] = decode['roles']
        users_socket[sid] = decode['user']
        users_socket[sid]['sid'] = sid
        if decode['user']['id'] not in users_by_user_id:
            users_by_user_id[decode['user']['id']] = list()
        users_by_user_id[decode['user']['id']].append(sid)

        await sio.emit(ROUTES['FRONT']['AUTH'], {'data': decode['user']}, room=sid)

        await sio.emit(ROUTES['FRONT']['USER']['ALL'], {
            'data': await User.get_users_without_self(users_socket[sid]['id'])
        }, namespace='/')

        participated = await get_and_send_participated_by_user_id(sio, int(users_socket[sid]['id']), sid)

        if len(participated) == 0:
            participated = None

        await send_messages_by_chat_name(sio, sid, participated[0] if participated else None)

    @sio.on(ROUTES['BACK']['DISCONNECT'])
    async def disconnect(sid):

        if sid in users_socket:
            user = users_socket[sid]
            del users_by_user_id[user["id"]]
            sids_fir_remove = list()
            try:
                for user_data in users_socket:
                    if users_socket[user_data]['id'] == user['id']:
                        sids_fir_remove.append(user_data)

                for sid in sids_fir_remove:
                    del users_socket[sid]
                    del sio.environ[sid]

                if user:
                    await sio.emit(ROUTES['FRONT']['USER']['ONLINE'], {
                        'data': [users_by_user_id[user] for user in users_by_user_id]
                    }, namespace='/')
            except:
                pass

        return await sio.disconnect(sid)

    async def background_task():

        await sio.sleep(5)

        while True:
            try:
                await sio.sleep(5)
            except Exception as e:
                logger.exception('')

    return sio, background_task
