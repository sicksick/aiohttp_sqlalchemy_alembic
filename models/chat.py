import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from config import config
from helpers.irc import irc
from middleware.errors import CustomHTTPException
from models.role import Role
from models.user_group import UserGroup
Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


sa_chat = Chat.__table__
