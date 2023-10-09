"""add updated_on field

Revision ID: 2739ce675fc7
Revises: 377db01afe73
Create Date: 2023-10-05 23:54:50.127180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2739ce675fc7'
down_revision: Union[str, None] = '377db01afe73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('art', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('audio', sa.Column('updated_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audio', 'updated_on')
    op.drop_column('art', 'updated_on')
    # ### end Alembic commands ###