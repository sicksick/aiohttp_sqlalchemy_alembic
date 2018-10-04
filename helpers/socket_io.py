import logging

import jwt

from config.config import config

logger = logging.getLogger('Rotating Log')

users_socket = dict()


def get_socket_io_route(sio):
    @sio.on('my event')
    async def test_message(sid, message):
        await sio.emit('my response', {'data': message['data']}, room=sid)

    @sio.on('connect')
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
        users_socket[sid]['scraper'] = {
            'current_type_scraper': None
        }
        await sio.emit('auth', {'data': decode['user']}, room=sid)

    @sio.on('disconnect')
    async def disconnect(sid):
        if sid in users_socket:
            user = users_socket[sid]
            del users_socket[sid]
        return await sio.disconnect(sid)


    async def background_task():

        await sio.sleep(5)

        while True:
            try:
                await sio.sleep(5)
            except Exception as e:
                logger.exception('')

    return sio, background_task

