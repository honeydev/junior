"""empty message

Revision ID: 94cb730fe665
Revises: d6814cf6e6d5
Create Date: 2019-10-07 17:50:10.510583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94cb730fe665'
down_revision = 'd6814cf6e6d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_superuser')
    # ### end Alembic commands ###
