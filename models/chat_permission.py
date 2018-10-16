import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Integer, func, ForeignKey, desc
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base

from config import config
from helpers.db_helper import as_dict
from models.chat import sa_chat

Base = declarative_base()


class ChatPermission(Base):
    __tablename__ = 'chats_permission'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    permission = Column('permission',  ENUM('admin', 'user', 'guest', 'removed', name='chats_permission_enum'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_participated_by_user_id(user_id: int) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_chat_permission.c.permission,
                               sa_chat.c.id,
                               sa_chat.c.name,
                               sa_chat.c.created_at
                               ]) \
                .select_from(
                    sa_chat_permission.join(sa_chat, sa_chat_permission.c.chat_id == sa_chat.c.id, isouter=True)
                ) \
                .where(sa_chat_permission.c.user_id == user_id) \
                .order_by(desc(sa_chat.c.created_at))
            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))


sa_chat_permission = ChatPermission.__table__
