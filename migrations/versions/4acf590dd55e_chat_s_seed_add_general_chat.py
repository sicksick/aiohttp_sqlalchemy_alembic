"""chat's seed - add general chat

Revision ID: 4acf590dd55e
Revises: 014e2778ec23
Create Date: 2018-10-06 20:39:38.760084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from models.chat import sa_chat

revision = '4acf590dd55e'
down_revision = '014e2778ec23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(sa_chat,
        [
            {'name': 'general'},
        ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('TRUNCATE chats CASCADE ;')
    # ### end Alembic commands ###
