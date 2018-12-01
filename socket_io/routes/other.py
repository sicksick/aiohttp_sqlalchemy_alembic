from socket_io.config import ROUTES


def get_other_routes(sio, app):

    @sio.on(ROUTES['BACK']['MY_EVENT'])
    async def test_message(sid):
        print(ROUTES['BACK']['MY_EVENT'])
