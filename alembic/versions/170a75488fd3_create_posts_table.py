"""create posts table

Revision ID: 170a75488fd3
Revises: 
Create Date: 2023-12-10 11:39:51.464886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "170a75488fd3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     pass
def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass


# def downgrade() -> None:
#     pass
