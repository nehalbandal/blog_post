"""empty message

Revision ID: e690d3ed23dd
Revises: 3360b1ce4afd
Create Date: 2020-08-25 02:39:59.914600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e690d3ed23dd'
down_revision = '3360b1ce4afd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_category'))
    )
    op.create_table('categories',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['category.id'], name=op.f('fk_categories_cat_id_category')),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_categories_post_id_post')),
    sa.PrimaryKeyConstraint('cat_id', 'post_id', name=op.f('pk_categories'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categories')
    op.drop_table('category')
    # ### end Alembic commands ###