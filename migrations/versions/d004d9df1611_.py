"""empty message

Revision ID: d004d9df1611
Revises: e8b205282abb
Create Date: 2021-02-27 17:29:30.290411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd004d9df1611'
down_revision = 'e8b205282abb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('phfcc_messages', 'frequency')
    op.drop_column('phfcc_messages', 'day_of_week')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phfcc_messages', sa.Column('day_of_week', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('phfcc_messages', sa.Column('frequency', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###