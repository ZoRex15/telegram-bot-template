"""Added mailings table

Revision ID: fdac1dae4f48
Revises: c258fa29f42f
Create Date: 2025-02-18 20:36:34.277244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdac1dae4f48'
down_revision: Union[str, None] = 'c258fa29f42f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Mailings',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('tg_image_id', sa.VARCHAR(length=128), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'PROCESSED', 'FINALIZED', 'STOPPED', name='mailingstatus'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('ended_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Mailings')
    # ### end Alembic commands ###
