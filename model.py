from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, nullable=False)
    role = Column(String, nullable=False)


class UserGroups(Base):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)


sa_user_group = UserGroups.__table__
sa_group = Group.__table__
sa_user = User.__table__
