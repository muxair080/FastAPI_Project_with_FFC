"""create post table

Revision ID: 5075a2bdd47c
Revises: 
Create Date: 2022-02-27 11:01:07.016171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5075a2bdd47c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id' , sa.Integer(), nullable= False , primary_key= True),
    sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
