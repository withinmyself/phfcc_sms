"""empty message

Revision ID: 5e6d609b0370
Revises: d004d9df1611
Create Date: 2021-02-27 19:59:17.545578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e6d609b0370'
down_revision = 'd004d9df1611'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'phfcc_members', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'phfcc_members', type_='unique')
    # ### end Alembic commands ###
