"""empty message

Revision ID: 4e2f94c2292c
Revises: None
Create Date: 2014-12-08 20:53:01.811050

"""

# revision identifiers, used by Alembic.
revision = '4e2f94c2292c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('content', sa.Unicode(length=24), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unified_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('identity', sa.String(length=64), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('idol_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unified_user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel', sa.Unicode(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_comment_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unified_user_id', sa.Integer(), nullable=False),
    sa.Column('post_comment_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.Unicode(length=10), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('salt', sa.String(length=128), nullable=False),
    sa.Column('sex', sa.SmallInteger(), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('identity', sa.String(length=64), nullable=False),
    sa.Column('golds', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.String(length=128), nullable=False),
    sa.Column('signature', sa.Unicode(length=30), nullable=False),
    sa.Column('push', sa.Boolean(), nullable=False),
    sa.Column('disturb', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_shares',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unified_user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('society_id', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('third_party_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('society_user_id', sa.String(length=32), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('society_id', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=128), nullable=False),
    sa.Column('content', sa.Unicode(length=140), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('likes_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_comment_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_comment_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('societies',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('society', sa.Unicode(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_reports')
    op.drop_table('societies')
    op.drop_table('post_comment_reports')
    op.drop_table('posts')
    op.drop_table('third_party_users')
    op.drop_table('post_shares')
    op.drop_table('users')
    op.drop_table('collections')
    op.drop_table('post_comment_likes')
    op.drop_table('channels')
    op.drop_table('post_likes')
    op.drop_table('fans')
    op.drop_table('unified_users')
    op.drop_table('post_comments')
    ### end Alembic commands ###
