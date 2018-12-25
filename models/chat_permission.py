import sqlalchemy as sa
from aiopg.sa import SAConnection
from sqlalchemy import Column, DateTime, Integer, func, ForeignKey, desc, or_, Text, and_, asc, literal_column, String, \
    text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import label
from config import config
from helpers.db_helper import as_dict, raise_db_exception
from helpers.irc import irc
from middleware.errors import CustomHTTPException
from models.chat import sa_chat
from models.message import sa_message

Base = declarative_base()


class ChatPermission(Base):
    __tablename__ = 'chats_permission'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    permission = Column('permission', ENUM('admin', 'user', 'guest', 'removed', name='chats_permission_enum'))
    chat_image = Column(Text, default='/media/avatars/default_group.png')
    chat_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_participated_by_user_id(user_id: int) -> list:
        async with config['db'].acquire() as conn:
            message_id = sa.select([sa_message.c.id]) \
                .select_from(sa_message) \
                .where(sa_chat.c.id == sa_message.c.chat_id) \
                .order_by(desc(sa_message.c.id)) \
                .limit(1) \
                .as_scalar()

            query = sa.select([sa_chat_permission.c.id.label('chat_permission_id'),
                               sa_chat_permission.c.permission,
                               sa_chat_permission.c.chat_name,
                               sa_chat_permission.c.chat_image,
                               sa_chat.c.id.label('chat_id'),
                               sa_chat.c.created_at,
                               message_id.label('message_id')

                               ]) \
                .select_from(
                sa_chat
                    .join(sa_chat_permission, sa_chat_permission.c.chat_id == sa_chat.c.id, isouter=True)
            ) \
                .where(or_(sa_chat_permission.c.user_id == user_id, sa_chat_permission.c.user_id == None)) \
                .order_by(asc('message_id'))

            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

    @staticmethod
    async def get_participated_by_user_id_and_chat_id(chat_id: int, user_id: int) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_chat_permission.c.id.label('chat_permission_id'),
                               sa_chat_permission.c.permission,
                               sa_chat_permission.c.chat_image,
                               sa_chat_permission.c.chat_name,
                               sa_chat.c.id.label('chat_id'),
                               sa_chat.c.created_at,
                               ]) \
                .select_from(
                    sa_chat
                    .join(sa_chat_permission, sa_chat_permission.c.chat_id == sa_chat.c.id, isouter=True)
                ) \
                .where(
                    and_(
                        or_(sa_chat_permission.c.user_id == user_id, sa_chat_permission.c.user_id == None),
                        sa_chat_permission.c.chat_id == chat_id
                    )
                )

            return list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))

    # @staticmethod
    # async def get_chat_id_by_user_id_list(users_id: list) -> int or None:
    #     async with config['db'].acquire() as conn:
    #         query = sa.select([sa_chat_permission.c.chat_id]) \
    #             .select_from(sa_chat_permission) \
    #             .where(sa_chat_permission.c.user_id.in_(users_id)) \
    #             .group_by(sa_chat_permission.c.chat_id) \
    #             .having(func.count(sa_chat_permission.c.chat_id) == len(users_id))
    #
    #         users_participated = list(map(lambda x: as_dict(dict(x)), await conn.execute(query)))
    #         return users_participated[0]['chat_id'] if len(users_participated) > 0 else None

    @staticmethod
    async def get_chat_id_by_user_id_list(users_id: list) -> list:
        async with config['db'].acquire() as conn:
            query = text("""
                SELECT chat_id
                from (SELECT
                        cp.chat_id,
                        count(cp.chat_id) as found_members,
                        (select count(cps.id) as all_members
                         from chats_permission cps
                         where cp.chat_id = cps.chat_id
                        )                 as all_members
                      FROM chats
                             left join chats_permission cp on chats.id = cp.chat_id
                      where cp.user_id IN :users_id
                      group by cp.chat_id) as list
                where list.found_members = :users_count
                  and list.all_members = :users_count;
            """)
            users_participated = list(map(lambda x: as_dict(dict(x)), await conn.execute(query,
                                                                                         users_id=tuple(users_id),
                                                                                         users_count=len(users_id))))
            return users_participated[0]['chat_id'] if len(users_participated) == 1 else None

    @staticmethod
    async def create_chat_permission_bulk(chat_permissions: list, connect: SAConnection) -> dict or None:
        try:
            query = sa_chat_permission.insert(inline=True)
            query = query.values(chat_permissions).returning(literal_column('*'))
            new_permissions = [as_dict(dict(chat_permission))
                               for chat_permission in (await (await connect.execute(query)).fetchall())]

            if not new_permissions:
                raise CustomHTTPException(irc['INTERNAL_SERVER_ERROR'], 500)

            return new_permissions
        except Exception as e:
            raise await raise_db_exception(e)

    @staticmethod
    async def get_last_participated_by_user_id(user_id: int) -> dict or None:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_chat_permission.c.permission,
                               label('chat_id', sa_chat.c.id),
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
