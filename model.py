import datetime

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from config import config
from helpers.irc import irc
from middleware.errors import CustomHTTPException

Base = declarative_base()


async def as_dict(obj):
    if isinstance(obj, list):
        for items in obj:
            for item in items:
                if isinstance(items[item], datetime.datetime):
                    items[item] = str(items[item])
                if isinstance(items[item], datetime.timedelta):
                    items[item] = str(items[item])
        return obj
    if isinstance(obj, dict):
        for item in obj:
            if isinstance(obj[item], datetime.datetime):
                obj[item] = str(obj[item])
            if isinstance(obj[item], datetime.timedelta):
                obj[item] = str(obj[item])
        return obj
    return obj


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    image = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)
    google_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_user_by_facebook_id(facebook_id: str) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_user.c.id,
                               sa_user.c.email,
                               sa_user.c.password,
                               sa_user.c.firstname,
                               sa_user.c.lastname,
                               sa_user.c.image
                               ]) \
                .select_from(sa_user) \
                .where(sa_user.c.facebook_id == facebook_id)
            users = list(map(lambda x: dict(x), await conn.execute(query)))
            return users[0] if len(users) == 1 else None

    @staticmethod
    async def get_user_by_google_id(google_id: str) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_user.c.id,
                               sa_user.c.email,
                               sa_user.c.password,
                               sa_user.c.firstname,
                               sa_user.c.lastname,
                               sa_user.c.image
                               ]) \
                .select_from(sa_user) \
                .where(sa_user.c.google_id == google_id)
            users = list(map(lambda x: dict(x), await conn.execute(query)))
            return users[0] if len(users) == 1 else None

    @staticmethod
    async def get_user_by_email(email: str) -> list:
        async with config['db'].acquire() as conn:
            query = sa.select([sa_user.c.id,
                               sa_user.c.email,
                               sa_user.c.password,
                               sa_user.c.firstname,
                               sa_user.c.lastname,
                               sa_user.c.image
                               ]) \
                .select_from(sa_user) \
                .where(sa_user.c.email == email)
            return list(map(lambda x: dict(x), await conn.execute(query)))

    @staticmethod
    async def get_user_by_id(user_id: int):
        async with config['db'].acquire() as conn:
            query = sa.select([sa_user.c.id,
                               sa_user.c.email,
                               sa_user.c.password,
                               sa_user.c.firstname,
                               sa_user.c.lastname,
                               sa_user.c.image
                               ]) \
                .select_from(sa_user) \
                .where(sa_user.c.id == user_id)
            users = list(map(lambda x: dict(x), await conn.execute(query)))
            return users[0] if len(users) == 1 else None

    @staticmethod
    async def create_user(data: dict) -> int:
        if 'roles' not in data:
            raise CustomHTTPException(irc['ACCESS_DENIED'], 401)
        roles = data['roles']
        del data['roles']
        async with config['db'].acquire() as conn:
            query = sa_user.insert().values(data)
            user = list(map(lambda x: dict(x), await conn.execute(query)))
            if len(user) != 1:
                raise CustomHTTPException(irc['INTERNAL_SERVER_ERROR'], 500)
            new_user_id = user[0]['id']

            for role in roles:
                found_role = await Role.get_role_by_name(role)
                if not found_role:
                    raise CustomHTTPException(irc['ROLE_NOT_FOUND'], 404)

                await UserGroup.add_role_to_user(new_user_id, found_role['id'])
        return new_user_id


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    @staticmethod
    async def get_roles_by_id(id: int) -> list:
        async with config['db'].acquire() as conn:
            query = text("""
                SELECT
                    r.name as name
                FROM user_groups
                left join roles r on user_groups.role_id = r.id
                where
                    user_groups.user_id = :id
                ;
            """)
            return list(map(lambda x: dict(x), await conn.execute(query, id=id)))

    @staticmethod
    async def get_role_by_name(role_name: str) -> list or None:
        async with config['db'].acquire() as conn:
            query = text("""
                SELECT
                    roles.*
                FROM roles
                where
                    roles.name = :role_name
                ;
            """)
            roles = list(map(lambda x: dict(x), await conn.execute(query, role_name=role_name)))
            if len(roles) == 1:
                return roles[0]
            return None


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
sa_role = Role.__table__
sa_user = User.__table__
