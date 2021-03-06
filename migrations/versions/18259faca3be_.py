"""empty message

Revision ID: 18259faca3be
Revises: 3bf3d6f9cb58
Create Date: 2014-12-21 23:34:36.629513

"""

# revision identifiers, used by Alembic.
revision = '18259faca3be'
down_revision = '3bf3d6f9cb58'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_types',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('message_type_id', sa.SmallInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('launch_id', sa.Integer(), nullable=False),
    sa.Column('post_comment_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('message_types')
    ### end Alembic commands ###
