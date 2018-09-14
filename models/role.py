from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from config import config
Base = declarative_base()


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


sa_role = Role.__table__
