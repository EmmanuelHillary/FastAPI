"""add user foreign key to posts table

Revision ID: 918f7f9b73d4
Revises: edf240ab5cc9
Create Date: 2021-11-28 19:59:38.484857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '918f7f9b73d4'
down_revision = 'edf240ab5cc9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_id_fkey", source_table="posts", referent_table="users", 
    local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint(
        "posts_user_id_fkey",
        table_name="posts"
    )
    op.drop_column("posts", "user_id")
    pass
