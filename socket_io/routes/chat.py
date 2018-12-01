from models.chat_permission import ChatPermission
from models.message import Message
from socket_io.helper import get_and_send_participated_by_user_id, send_messages_by_chat_name
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
        print(data)

        data['id'].append(users_socket[sid]['id'])

        participated_chat_id = await ChatPermission.get_participated_by_user_id_list(data['id'])

        if participated_chat_id:
            # Отдаем список с активным этим чатом и историей сообщений
            participated = await get_and_send_participated_by_user_id(sio, int(users_socket[sid]['id']), sid)
            active_chat = participated[0]

            for chat_item in participated:
                if chat_item['chat_id'] == participated_chat_id:
                    active_chat = chat_item

            return await send_messages_by_chat_name(sio, sid, active_chat)

        # создаем чат и отдаем список с активным этим чатом
        # Создать запись с картинкой учасника если учасников 2, если больше стандартную груповую картинку

    @sio.on(ROUTES['BACK']['CHAT']['REMOVE'])
    async def chat_remove(sid):
        print(ROUTES['BACK']['CHAT']['REMOVE'])

    @sio.on(ROUTES['BACK']['CHAT']['INVITE'])
    async def chat_invite(sid):
        print(ROUTES['BACK']['CHAT']['INVITE'])

    @sio.on(ROUTES['BACK']['CHAT']['CHANGE'])  # Переключение на другой чат
    async def chat_invite(sid, data):
        print(ROUTES['BACK']['CHAT']['CHANGE'])
        print(data)

        participated = await get_and_send_participated_by_user_id(sio, int(users_socket[sid]['id']), sid)
        active_chat = participated[0]

        for chat_item in participated:
            if chat_item['chat_id'] == int(data['id']):
                active_chat = chat_item

        await send_messages_by_chat_name(sio, sid, active_chat)

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
