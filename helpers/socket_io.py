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
            logger.exception('')
            return
        decode['user']['roles'] = decode['roles']
        del decode['user']['password']
        decode['user']['status'] = 'busy'
        users_socket[sid] = decode['user']
        users_socket[sid]['sid'] = sid
        await sio.emit('connect', {'data': decode['user']}, room=sid)

    @sio.on('disconnect')
    async def disconnect(sid):
        user = users_socket[sid]
        del users_socket[sid]

    async def background_task():

        await sio.sleep(5)

        while True:
            try:
                await sio.sleep(5)
            except Exception as e:
                logger.exception('')

    return sio, background_task

