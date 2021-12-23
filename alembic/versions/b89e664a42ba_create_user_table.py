"""create user table

Revision ID: b89e664a42ba
Revises: 25d7772419af
Create Date: 2021-12-23 10:41:38.007443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b89e664a42ba'
down_revision = '25d7772419af'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )
    pass


def downgrade():
    op.drop_table('users')
    pass
