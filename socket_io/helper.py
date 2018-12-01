from models.chat_permission import ChatPermission
from models.message import Message
from socket_io.socket_config import ROUTES, users_socket


async def send_messages_by_chat_name(sio, sid: str, active_participated=None) -> None:
    if not active_participated:
        return await sio.emit(ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY'], {
            'data': {
                'messages': [],
                'chat': {}
            }
        }, room=sid)

    first_participated_messages = await Message.get_messages_by_chat_name(active_participated['name'])
    return await sio.emit(ROUTES['FRONT']['CHAT']['MESSAGE']['HISTORY'], {
        'data': {
            'messages': first_participated_messages,
            'chat': active_participated
        }
    }, room=sid)


async def get_and_send_participated_by_user_id(sio, user_id: int, sid: str) -> list:
    participated = await ChatPermission.get_participated_by_user_id(int(user_id))
    await sio.emit(ROUTES['FRONT']['CHAT']['PARTICIPATED'], {'data': participated}, room=sid)
    return participated
