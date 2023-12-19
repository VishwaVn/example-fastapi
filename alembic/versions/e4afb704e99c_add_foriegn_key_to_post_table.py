"""add foriegn key to post table

Revision ID: e4afb704e99c
Revises: 75cc09cc4b71
Create Date: 2023-12-19 18:00:36.220579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e4afb704e99c"
down_revision: Union[str, None] = "75cc09cc4b71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )

    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
