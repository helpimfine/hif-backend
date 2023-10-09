"""Added url fields.

Revision ID: 7ec0e5ea854c
Revises: a38a8078be31
Create Date: 2023-10-06 13:16:18.160532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec0e5ea854c'
down_revision: Union[str, None] = 'a38a8078be31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('art', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('audio', sa.Column('audio_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audio', 'audio_url')
    op.drop_column('art', 'image_url')
    # ### end Alembic commands ###
