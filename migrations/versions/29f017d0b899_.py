"""empty message

Revision ID: 29f017d0b899
Revises: 2c2b25add54d
Create Date: 2015-06-11 17:08:11.619327

"""

# revision identifiers, used by Alembic.
revision = '29f017d0b899'
down_revision = '2c2b25add54d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'privileges', ['username'])
    op.add_column('users', sa.Column('username', sa.Unicode(length=15), nullable=False))
    op.drop_column('users', 'email_confirmed')
    op.drop_column('users', 'email')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', mysql.VARCHAR(length=64), nullable=False))
    op.add_column('users', sa.Column('email_confirmed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('users', 'username')
    op.drop_constraint(None, 'privileges', type_='unique')
    ### end Alembic commands ###
