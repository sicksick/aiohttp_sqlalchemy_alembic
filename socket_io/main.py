import logging

import jwt

from config.config import config
from models.chat_permission import ChatPermission
from models.message import Message
from models.user import User
from socket_io.routes.chat import get_chat_routes
from socket_io.routes.other import get_other_routes
from socket_io.socket_config import ROUTES, users_socket, users_by_user_id
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
        users_by_user_id[decode['user']['id']] = users_socket[sid]

        await sio.emit(ROUTES['FRONT']['AUTH'], {'data': decode['user']}, room=sid)

        await sio.emit(ROUTES['FRONT']['USER']['ALL'], {
            'data': await User.get_users()
        }, namespace='/')

        participated = await ChatPermission.get_participated_by_user_id(int(users_socket[sid]['id']))
        await sio.emit(ROUTES['FRONT']['CHAT']['PARTICIPATED'], {'data': participated}, room=sid)

        if len(participated) != 0:
            first_participated_messages = await Message.get_messages_by_chat_name(participated[0]['name'])
            await sio.emit(ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY'], {
                'data': {
                    'messages': first_participated_messages,
                    'chat': participated[0]
                }
            }, room=sid)
            users_socket[sid]['active_chat'] = participated[0]

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
            except:
                pass

        await sio.emit(ROUTES['FRONT']['USER']['ONLINE'], {
            'data': [users_by_user_id[user] for user in users_by_user_id]
        }, namespace='/')

        return await sio.disconnect(sid)

    async def background_task():

        await sio.sleep(5)

        while True:
            try:
                await sio.sleep(5)
            except Exception as e:
                logger.exception('')

    return sio, background_task
