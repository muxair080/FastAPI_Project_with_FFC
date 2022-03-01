"""add last few columns to posts table

Revision ID: 8c22f5418f1b
Revises: 3c6c6595b5bb
Create Date: 2022-02-27 11:33:19.516718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c22f5418f1b'
down_revision = '3c6c6595b5bb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts' , sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts' , sa.Column('Created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default= sa.text('NOW()')))

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
