import datetime
import sqlalchemy as sa
from sqlalchemy import ForeignKey

meta = sa.MetaData()


user = sa.Table(
    'users', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String),
    sa.Column('password', sa.String),
    sa.Column('name', sa.String, nullable=True),
    sa.Column('created_at', sa.DateTime, default=datetime.datetime.now),
    sa.Column('updated_at', sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
)

group = sa.Table(
    'groups', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('role', sa.String, nullable=False),
)

user_group = sa.Table(
    'user_groups', meta,
    sa.Column('user_id', sa.Integer, ForeignKey('users.id'), nullable=False),
    sa.Column('group_id', sa.Integer, ForeignKey('groups.id'), nullable=False)
)

