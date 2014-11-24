"""empty message

Revision ID: 4d2b51280bb5
Revises: 2f93be9ae6e
Create Date: 2014-11-24 23:41:11.947822

"""

# revision identifiers, used by Alembic.
revision = '4d2b51280bb5'
down_revision = '2f93be9ae6e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('disturb', sa.Boolean(), nullable=False))
    op.drop_column('users', 'no_disturb')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('no_disturb', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('users', 'disturb')
    ### end Alembic commands ###
