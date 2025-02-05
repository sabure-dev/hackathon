"""leaderboard add

Revision ID: 128d5b0baedb
Revises: 5e22f86068ad
Create Date: 2025-02-05 17:45:56.602338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '128d5b0baedb'
down_revision: Union[str, None] = '5e22f86068ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaderboard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('games', sa.Integer(), nullable=False),
    sa.Column('wins', sa.Integer(), nullable=False),
    sa.Column('losses', sa.Integer(), nullable=False),
    sa.Column('scored', sa.Integer(), nullable=False),
    sa.Column('conceded', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaderboard_id'), 'leaderboard', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leaderboard_id'), table_name='leaderboard')
    op.drop_table('leaderboard')
    # ### end Alembic commands ###
