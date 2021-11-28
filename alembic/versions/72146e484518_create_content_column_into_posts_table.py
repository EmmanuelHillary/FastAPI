"""create content column into posts table

Revision ID: 72146e484518
Revises: 18850e8a40a7
Create Date: 2021-11-28 17:26:06.190004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72146e484518'
down_revision = '18850e8a40a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
