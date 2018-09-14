from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config import config
from helpers.irc import irc
from middleware.errors import CustomHTTPException
Base = declarative_base()


class UserGroup(Base):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    @staticmethod
    async def add_role_to_user(user_id: int, role_id: int) -> bool:
        async with config['db'].acquire() as conn:
            query = sa_user_group.insert().values({"user_id": user_id, "role_id": role_id})
            result = list(map(lambda x: dict(x), await conn.execute(query)))
            if len(result) != 1:
                raise CustomHTTPException(irc['INTERNAL_SERVER_ERROR'], 500)
            return True


sa_user_group = UserGroup.__table__
