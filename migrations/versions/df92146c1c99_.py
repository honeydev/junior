"""empty message

Revision ID: df92146c1c99
Revises: 837a82783686
Create Date: 2019-11-21 12:03:49.676761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df92146c1c99'
down_revision = '508843369a49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image')
    # ### end Alembic commands ###
