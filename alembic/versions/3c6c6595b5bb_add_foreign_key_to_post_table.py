"""add foreign key to post table

Revision ID: 3c6c6595b5bb
Revises: d6795eb8d87f
Create Date: 2022-02-27 11:23:58.368564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c6c6595b5bb'
down_revision = 'd6795eb8d87f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk' , source_table='posts', referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts',"owner_id")
    pass
