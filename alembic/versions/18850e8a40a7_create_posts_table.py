"""create posts table

Revision ID: 18850e8a40a7
Revises: 
Create Date: 2021-11-28 17:05:47.700269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18850e8a40a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=True),
        sa.Column("title", sa.String(), nullable=False)
        )
    pass


def downgrade():
    op.drop_table("posts")
    pass
