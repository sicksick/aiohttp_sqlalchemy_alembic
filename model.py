import sqlalchemy as sa
from sqlalchemy import ForeignKey

meta = sa.MetaData()


user = sa.Table(
    'users', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('name', sa.String(255)))

question = sa.Table(
    'questions', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, ForeignKey('users.id')),
    sa.Column('question_text', sa.String(200), nullable=False),
    sa.Column('pub_date', sa.Date, nullable=False))

choice = sa.Table(
    'choice', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('question_id', sa.Integer, ForeignKey('questions.id'), nullable=False),
    sa.Column('choice_text', sa.String(200), nullable=False),
    sa.Column('votes', sa.Integer, server_default="0", nullable=False),
)


