from socket_io.config import ROUTES


def get_user_routes(sio, app):

    @sio.on(ROUTES['BACK']['USER']['INVITE'])
    async def user_invite(sid):
        print(ROUTES['BACK']['USER']['INVITE'])

    @sio.on(ROUTES['BACK']['USER']['EXCLUDE'])
    async def user_exclude(sid):
        print(ROUTES['BACK']['USER']['EXCLUDE'])
