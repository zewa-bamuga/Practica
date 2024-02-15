"""rating

Revision ID: 6739ae439f6f
Revises: 3774dff2ee2e
Create Date: 2024-02-15 14:52:18.249080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6739ae439f6f'
down_revision: Union[str, None] = '3774dff2ee2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('route_rating', sa.Column('question_id', sa.Integer(), nullable=True))
    op.drop_constraint('route_rating_survey_id_fkey', 'route_rating', type_='foreignkey')
    op.create_foreign_key(None, 'route_rating', 'question', ['question_id'], ['id'])
    op.drop_column('route_rating', 'survey_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('route_rating', sa.Column('survey_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'route_rating', type_='foreignkey')
    op.create_foreign_key('route_rating_survey_id_fkey', 'route_rating', 'survey', ['survey_id'], ['id'])
    op.drop_column('route_rating', 'question_id')
    # ### end Alembic commands ###