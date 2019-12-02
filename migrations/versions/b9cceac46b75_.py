"""empty message

Revision ID: b9cceac46b75
Revises: c7e984687a73
Create Date: 2019-12-02 10:05:25.788512

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as ps


# revision identifiers, used by Alembic.
revision = 'b9cceac46b75'
down_revision = 'c7e984687a73'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'gravatar')

    avatar_type = ps.ENUM('gravatar', 'face', '', name='avatar_type')
    avatar_type.create(op.get_bind())
    op.add_column('users', sa.Column('avatar_type', sa.Enum('gravatar', 'face', '', name='avatar_type'), nullable=True))


def downgrade():
    op.drop_column('users', 'avatar_type')
    avatar_type = ps.ENUM('gravatar', 'face', '', name='avatar_type')
    avatar_type.drop(op.get_bind())

    op.add_column('users', sa.Column('gravatar', sa.BOOLEAN(), autoincrement=False, nullable=True))
