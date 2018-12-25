from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, desc, asc, literal_column
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.sql import label

from config import config
from helpers.db_helper import as_dict, raise_db_exception
from helpers.irc import irc
from middleware.errors import CustomHTTPException
from models.chat import sa_chat
from models.user import sa_user

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=True)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_messages_by_chat_id(chat_id: int) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_message.c.id,
                               sa_message.c.user_id,
                               sa_message.c.text,
                               label('message_text', sa_message.c.text),
                               label('message_image', sa_message.c.image),
                               sa_message.c.created_at,
                               label('user_name', (sa_user.c.name)),
                               sa_user.c.email,
                               label('user_image', sa_user.c.image)
                               ]) \
                .select_from(
                    sa_message
                        .join(sa_chat, sa_message.c.chat_id == sa_chat.c.id, isouter=True)
                        .join(sa_user, sa_message.c.user_id == sa_user.c.id, isouter=True)
                ) \
                .where(sa_chat.c.id == chat_id) \
                .order_by(asc(sa_message.c.id))
            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

    @staticmethod
    async def new_messages_by_chat_id(message: str, chat_id: int, user_id: int) -> dict:
        try:
            query = sa_message.insert(inline=True)
            query = query.values([{
                'chat_id': chat_id,
                'text':message,
                'user_id': user_id
            }]).returning(literal_column('*'))
            async with config['db'].acquire() as conn:
                new_message = [as_dict(dict(message))
                                   for message in (await (await conn.execute(query)).fetchall())]

                if not new_message:
                    raise CustomHTTPException(irc['INTERNAL_SERVER_ERROR'], 500)

                query = sa.select([sa_message.c.id,
                                   sa_message.c.user_id,
                                   sa_message.c.text,
                                   label('message_text', sa_message.c.text),
                                   label('message_image', sa_message.c.image),
                                   sa_message.c.created_at,
                                   label('user_name', (sa_user.c.name)),
                                   sa_user.c.email,
                                   label('user_image', sa_user.c.image)
                                   ]) \
                    .select_from(
                    sa_message
                        .join(sa_chat, sa_message.c.chat_id == sa_chat.c.id)
                        .join(sa_user, sa_message.c.user_id == sa_user.c.id)
                    ) \
                    .where(sa_message.c.id == new_message[0]['id'])

                new_message_with_params = list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

                if len(new_message_with_params) != 0:
                    return new_message_with_params[0]
        except Exception as e:
            raise await raise_db_exception(e)


sa_message = Message.__table__
