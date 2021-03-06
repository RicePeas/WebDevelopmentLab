"""task table

Revision ID: 43693b7fec3a
Revises: ef64ac3690d7
Create Date: 2021-04-18 00:15:42.577434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43693b7fec3a'
down_revision = 'ef64ac3690d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('taskId', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('taskId')
    )
    op.create_index(op.f('ix_task_title'), 'task', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_title'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
