"""add content column to posts table

Revision ID: 2cb8972dc572
Revises: 170a75488fd3
Create Date: 2023-12-19 17:27:51.653070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2cb8972dc572"
down_revision: Union[str, None] = "170a75488fd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
