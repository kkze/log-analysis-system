"""Initial migration.

Revision ID: c7ca86d714f0
Revises: 
Create Date: 2024-03-27 18:46:41.135419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ca86d714f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('http_code', sa.Integer(), nullable=True),
    sa.Column('is_invalid', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    op.drop_table('log_entries')
    # ### end Alembic commands ###
