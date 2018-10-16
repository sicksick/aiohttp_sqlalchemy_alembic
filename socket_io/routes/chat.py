from socket_io.socket_config import ROUTES


def get_chat_routes(sio, app):

    @sio.on(ROUTES['BACK']['CHAT']['CREATE'])
    async def chat_invite(sid):
        print(ROUTES['BACK']['CHAT']['CREATE'])

    @sio.on(ROUTES['BACK']['CHAT']['REMOVE'])
    async def chat_remove(sid):
        print(ROUTES['BACK']['CHAT']['REMOVE'])

    @sio.on(ROUTES['BACK']['CHAT']['INVITE'])
    async def chat_invite(sid):
        print(ROUTES['BACK']['CHAT']['INVITE'])

    #MESSAGE
    @sio.on(ROUTES['BACK']['CHAT']['MESSAGE']['SEND'])
    async def chat_message_send(sid):
        print(ROUTES['BACK']['CHAT']['MESSAGE']['SEND'])

    @sio.on(ROUTES['BACK']['CHAT']['MESSAGE']['EDIT'])
    async def chat_message_edit(sid):
        print(ROUTES['BACK']['CHAT']['MESSAGE']['EDIT'])

    @sio.on(ROUTES['BACK']['CHAT']['MESSAGE']['REMOVE'])
    async def chat_message_remove(sid):
        print(ROUTES['BACK']['CHAT']['MESSAGE']['REMOVE'])
