"""home work

Revision ID: 6d69a051a668
Revises: 
Create Date: 2024-02-10 21:39:48.952579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d69a051a668'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_token_access_token', table_name='token')
    op.drop_table('token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='token_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='token_pkey')
    )
    op.create_index('ix_token_access_token', 'token', ['access_token'], unique=True)
    # ### end Alembic commands ###