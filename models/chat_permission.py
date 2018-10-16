from sqlalchemy import Column, DateTime, Integer, func, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatPermission(Base):
    __tablename__ = 'chats_permission'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    permission = Column('permission',  ENUM('admin', 'user', 'guest', 'removed', name='chats_permission_enum'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


sa_chat_permission = ChatPermission.__table__
