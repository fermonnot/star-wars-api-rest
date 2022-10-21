"""empty message

Revision ID: f9ec9e9411cd
Revises: ac4d2decbd60
Create Date: 2022-10-21 10:49:25.075868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ec9e9411cd'
down_revision = 'ac4d2decbd60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('favorites_id_user_fkey', 'favorites', type_='foreignkey')
    op.create_foreign_key(None, 'favorites', 'user', ['user_id'], ['id'])
    op.drop_column('favorites', 'id_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorites', sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'favorites', type_='foreignkey')
    op.create_foreign_key('favorites_id_user_fkey', 'favorites', 'user', ['id_user'], ['id'])
    op.drop_column('favorites', 'user_id')
    # ### end Alembic commands ###
