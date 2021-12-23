"""create content column in posts table

Revision ID: 25d7772419af
Revises: 1d8b7931bf21
Create Date: 2021-12-23 10:36:01.187831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d7772419af'
down_revision = '1d8b7931bf21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
