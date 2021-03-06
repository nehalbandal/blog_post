"""empty message

Revision ID: e376c1cd92a3
Revises: e690d3ed23dd
Create Date: 2020-08-28 00:59:32.714529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e376c1cd92a3'
down_revision = 'e690d3ed23dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], name=op.f('fk_followers_followed_id_user')),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name=op.f('fk_followers_follower_id_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
