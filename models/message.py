from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, desc, asc
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.sql import label

from config import config
from helpers.db_helper import as_dict
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
    async def get_messages_by_chat_name(name: str) -> list:
        from models.chat_permission import sa_chat_permission
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
                        .join(sa_chat_permission, sa_message.c.chat_id == sa_chat_permission.c.chat_id, isouter=True)
                        .join(sa_user, sa_message.c.user_id == sa_user.c.id, isouter=True)
                ) \
                .where(sa_chat_permission.c.chat_name == name) \
                .order_by(asc(sa_message.c.id))
            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))


sa_message = Message.__table__
