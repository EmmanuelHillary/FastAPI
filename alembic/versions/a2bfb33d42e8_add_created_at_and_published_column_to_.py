"""Add created at and published column to posts table

Revision ID: a2bfb33d42e8
Revises: 918f7f9b73d4
Create Date: 2021-11-28 20:16:15.463866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2bfb33d42e8'
down_revision = '918f7f9b73d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column(
        "posts", 
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False)
    )

def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
