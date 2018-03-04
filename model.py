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

permission_user = sa.Table(
    'user_permission', meta,
    sa.Column('user_id', sa.Integer, ForeignKey('users.id'), nullable=False),
    sa.Column('permission_id', sa.Integer, ForeignKey('permissions.id'), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
)

permission = sa.Table(
    'permissions', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('role', sa.String, nullable=False)
)


