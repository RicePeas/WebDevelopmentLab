"""empty message

Revision ID: 379da295b4d7
Revises: 43693b7fec3a
Create Date: 2021-04-30 04:18:33.594491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '379da295b4d7'
down_revision = '43693b7fec3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin_status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin_status')
    # ### end Alembic commands ###
