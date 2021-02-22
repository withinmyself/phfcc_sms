"""empty message

Revision ID: 75481993bd52
Revises: d1146ee14c90
Create Date: 2021-02-21 05:39:31.889578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75481993bd52'
down_revision = 'd1146ee14c90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('is_subscriber', sa.Boolean(), nullable=True))
    op.drop_column('members', 'subscriber')
    op.add_column('messages', sa.Column('day_of_week', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'day_of_week')
    op.add_column('members', sa.Column('subscriber', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('members', 'is_subscriber')
    # ### end Alembic commands ###
