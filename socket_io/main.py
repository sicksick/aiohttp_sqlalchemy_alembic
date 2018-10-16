import logging

import jwt

from config.config import config
from models.chat_permission import ChatPermission
from socket_io.routes.chat import get_chat_routes
from socket_io.routes.other import get_other_routes
from socket_io.socket_config import ROUTES, users_socket
from socket_io.routes.user import get_user_routes

logger = logging.getLogger('Rotating Log')


def get_socket_io_route(sio, app):

    get_user_routes(sio, app)

    get_chat_routes(sio, app)

    get_other_routes(sio, app)

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

        await sio.emit(ROUTES['FRONT']['AUTH'], {'data': decode['user']}, room=sid)

        await sio.emit(ROUTES['FRONT']['USER']['ONLINE'], {
            'data': [users_socket[user] for user in users_socket if int(users_socket[user]['id']) != int(users_socket[sid]['id'])]
        }, room=sid)

        participated = await ChatPermission.get_participated_by_user_id(int(users_socket[sid]['id']))
        await sio.emit(ROUTES['FRONT']['CHAT']['PARTICIPATED'], {'data': participated}, room=sid)

        # TODO get messages history from participated list
        await sio.emit(ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY'], {'data': ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY']}, room=sid)

    @sio.on(ROUTES['BACK']['DISCONNECT'])
    async def disconnect(sid):
        if sid in users_socket:
            user = users_socket[sid]
            sids_fir_remove = list()
            try:
                for user_data in users_socket:
                    if users_socket[user_data]['id'] == user['id']:
                        sids_fir_remove.append(user_data)

                for sid in sids_fir_remove:
                    del users_socket[sid]
                    del sio.environ[sid]
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
