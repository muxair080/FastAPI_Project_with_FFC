"""add user table

Revision ID: d6795eb8d87f
Revises: 7e7275377cf3
Create Date: 2022-02-27 11:09:44.975183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6795eb8d87f'
down_revision = '7e7275377cf3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), 
    sa.Column('email', sa.String(),nullable=False), 
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False), sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
    pass
