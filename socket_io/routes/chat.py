from config import config
from models.chat import Chat
from models.chat_permission import ChatPermission
from models.user import User
from socket_io.helper import send_participated_by_user_id_and_send_messages
from socket_io.config import ROUTES, users_socket, users_by_user_id


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
        users_id = data['id']
        users_id.append(users_socket[sid]['id'])
        participated_chat_id = await ChatPermission.get_chat_id_by_user_id_list(users_id)

        if participated_chat_id:
            # Отдаем список с активным этим чатом и историей сообщений
            # так как чат уже существует
            return await send_participated_by_user_id_and_send_messages(sio, sid, participated_chat_id)

        # создаем чат и отдаем список с активным этим чатом
        users = await User.get_users_by_id_list(users_id)
        default_image = False if len(users) == 2 else True

        chat_permission_bulk = []
        chat_name = ''
        user_admin = users_id[-1]
        
        for user in users:
            chat_name += f" {user['firstname'] if 'firstname' in user else user['email']}"

        async with config['db'].acquire() as connection:
            try:
                trans = await connection.begin()
                chat = await Chat.create_new_chat_by_name(connection)
                if default_image is True:
                    for user in users:
                        permission_for_insert = {
                            "chat_id": chat['id'],
                            "user_id": user['id'],
                            "chat_name": chat_name,
                            "permission": "user"
                        }

                        if user['id'] == user_admin:
                            permission_for_insert['permission'] = 'admin'

                        chat_permission_bulk.append(permission_for_insert)
                else:
                    chat_permission_bulk.append({
                        "chat_id": chat['id'],
                        "user_id": users[0]['id'],
                        "permission": "admin" if users[0]['id'] == user_admin else "user",
                        "chat_image": users[1]['image'],
                        "chat_name": users[1]['firstname'] if 'firstname' in users[1] else users[1]['email']
                    })
                    chat_permission_bulk.append({
                        "chat_id": chat['id'],
                        "user_id": users[1]['id'],
                        "permission": "admin" if users[1]['id'] == user_admin else "user",
                        "chat_image": users[0]['image'],
                        "chat_name": users[0]['firstname'] if 'firstname' in users[0] else users[0]['email']
                    })

                new_chat_permissions = await ChatPermission.create_chat_permission_bulk(chat_permission_bulk, connection)

                await trans.commit()

                for new_chat_permission in new_chat_permissions:
                    if new_chat_permission['user_id'] in users_by_user_id:
                        for online_user_sid in users_by_user_id[new_chat_permission['user_id']]:
                            await send_participated_by_user_id_and_send_messages(sio, online_user_sid, int(new_chat_permission['chat_id']))

            except Exception as e:
                await trans.rollback()
                raise e

    @sio.on(ROUTES['BACK']['CHAT']['REMOVE'])
    async def chat_remove(sid):
        print(ROUTES['BACK']['CHAT']['REMOVE'])

    @sio.on(ROUTES['BACK']['CHAT']['INVITE'])
    async def chat_invite(sid):
        print(ROUTES['BACK']['CHAT']['INVITE'])

    """
    Переключение на другой чат
    """
    @sio.on(ROUTES['BACK']['CHAT']['CHANGE'])
    async def chat_invite(sid, data):
        print(ROUTES['BACK']['CHAT']['CHANGE'])
        print(data)
        return await send_participated_by_user_id_and_send_messages(sio, sid, int(data['id']))

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
