from models.chat_permission import ChatPermission
from models.message import Message
from socket_io.socket_config import ROUTES, users_socket


def get_chat_routes(sio, app):

    """
    Создать чат с другим пользователь
    :return:
        - отправить список пользователей, не включая себя;
        - отправить список с чатами.
    """
    @sio.on(ROUTES['BACK']['CHAT']['CREATE'])
    async def chat_invite(sid, data):
        print(ROUTES['BACK']['CHAT']['CREATE'])

    @sio.on(ROUTES['BACK']['CHAT']['REMOVE'])
    async def chat_remove(sid):
        print(ROUTES['BACK']['CHAT']['REMOVE'])

    @sio.on(ROUTES['BACK']['CHAT']['INVITE'])
    async def chat_invite(sid):
        print(ROUTES['BACK']['CHAT']['INVITE'])

    @sio.on(ROUTES['BACK']['CHAT']['CHANGE'])  # Переключение на другой чат
    async def chat_invite(sid, data):
        participated = await ChatPermission.get_participated_by_user_id(int(users_socket[sid]['id']))
        active_index = 0
        for index, element in enumerate(participated):
            if int(element['chat_id']) == int(data['id']):
                element['active'] = True
                active_index = index

        if len(participated) != 0:
            first_participated_messages = await Message.get_messages_by_chat_name(participated[active_index]['name'])
            await sio.emit(ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY'], {
                'data': {
                    'messages': first_participated_messages,
                    'chat': participated[active_index]
                }
            }, room=sid)

        await sio.emit(ROUTES['FRONT']['CHAT']['PARTICIPATED'], {'data': participated}, room=sid)
        print(ROUTES['BACK']['CHAT']['CHANGE'])
        print(data)

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
