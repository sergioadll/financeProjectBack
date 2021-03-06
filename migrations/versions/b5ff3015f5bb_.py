"""empty message

Revision ID: b5ff3015f5bb
Revises: f86886746cce
Create Date: 2020-09-12 16:16:22.778003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5ff3015f5bb'
down_revision = 'f86886746cce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('watch_element', sa.Column('watchlist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'watch_element', 'watch_list', ['watchlist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'watch_element', type_='foreignkey')
    op.drop_column('watch_element', 'watchlist_id')
    # ### end Alembic commands ###
