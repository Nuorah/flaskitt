"""posts table

Revision ID: 7cfd21f1e49b
Revises: b1c31bca6e8a
Create Date: 2019-02-20 17:18:53.876822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cfd21f1e49b'
down_revision = 'b1c31bca6e8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.add_column('user', sa.Column('karma', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'karma')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
