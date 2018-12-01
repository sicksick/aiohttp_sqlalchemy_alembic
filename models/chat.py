from aiopg.sa import SAConnection
from sqlalchemy import Column, DateTime, Integer, String, func, text, literal_column
from sqlalchemy.ext.declarative import declarative_base
from helpers.db_helper import raise_db_exception, as_dict
from helpers.irc import irc
from middleware.errors import CustomHTTPException


Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def create_new_chat_by_name(name: str, connect: SAConnection) -> dict:
        try:
            query = sa_chat.insert(inline=True)
            query = query.values([{'name': name.strip()}]).returning(literal_column('*'))
            new_chat = as_dict(dict((await (await connect.execute(query)).fetchall())[0]))

            if not new_chat:
                raise CustomHTTPException(irc['INTERNAL_SERVER_ERROR'], 500)

            return new_chat
        except Exception as e:
            raise await raise_db_exception(e)


sa_chat = Chat.__table__
