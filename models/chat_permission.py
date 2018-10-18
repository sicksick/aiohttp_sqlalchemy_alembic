import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Integer, func, ForeignKey, desc, distinct
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import label

from config import config
from helpers.db_helper import as_dict
from models.chat import sa_chat
from models.message import sa_message

Base = declarative_base()


class ChatPermission(Base):
    __tablename__ = 'chats_permission'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    permission = Column('permission', ENUM('admin', 'user', 'guest', 'removed', name='chats_permission_enum'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_participated_by_user_id(user_id: int) -> list:
        async with config['db'].acquire() as conn:
            message_id = sa.select([sa_message.c.id])  \
                        .select_from(sa_message) \
                        .where(sa_chat.c.id == sa_message.c.chat_id)  \
                        .order_by(desc(sa_message.c.id))  \
                        .limit(1)\
                        .as_scalar()

            query = sa.select([sa_chat_permission.c.id.label('chat_permission_id'),
                               sa_chat_permission.c.permission,
                               sa_chat.c.id.label('chat_id'),
                               sa_chat.c.name,
                               sa_chat.c.created_at,
                               message_id.label('message_id')

                               ]) \
                .select_from(
                sa_chat
                    .join(sa_chat_permission, sa_chat_permission.c.chat_id == sa_chat.c.id, isouter=True)
            ) \
                .where(sa_chat_permission.c.user_id == user_id) \
                .order_by(desc('message_id'))

            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

    @staticmethod
    async def get_last_participated_by_user_id(user_id: int) -> dict or None:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_chat_permission.c.permission,
                               label('chat_id', sa_chat.c.id),
                               sa_chat.c.name,
                               sa_chat.c.created_at
                               ]) \
                .select_from(
                sa_chat_permission
                    .join(sa_chat, sa_chat_permission.c.chat_id == sa_chat.c.id, isouter=True)
                    .join(sa_message, sa_chat.c.id == sa_message.c.chat_id, isouter=True)
            ) \
                .where(sa_chat_permission.c.user_id == user_id) \
                .order_by(desc(sa_message.c.id)) \
                .limit(1)

            result = list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

            if len(result) != 0:
                return result[0]

            return None


sa_chat_permission = ChatPermission.__table__
