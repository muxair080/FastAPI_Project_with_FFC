"""add content table

Revision ID: 7e7275377cf3
Revises: 5075a2bdd47c
Create Date: 2022-02-27 11:06:17.484816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e7275377cf3'
down_revision = '5075a2bdd47c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
