"""empty message

Revision ID: 243b8fdb2de9
Revises: 93f05913ed5c
Create Date: 2019-10-03 23:14:50.687597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243b8fdb2de9'
down_revision = '93f05913ed5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('order_number', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'order_number')
    # ### end Alembic commands ###
