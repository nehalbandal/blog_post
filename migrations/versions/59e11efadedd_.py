"""empty message

Revision ID: 59e11efadedd
Revises: 07932ddc1c35
Create Date: 2020-08-18 01:56:24.721219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59e11efadedd'
down_revision = '07932ddc1c35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_idx', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('user_idx', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_comment_user_idx_user'), 'user', ['user_idx'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_comment_post_idx_post'), 'post', ['post_idx'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_comment_post_idx_post'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_comment_user_idx_user'), type_='foreignkey')
        batch_op.drop_column('user_idx')
        batch_op.drop_column('post_idx')

    # ### end Alembic commands ###
