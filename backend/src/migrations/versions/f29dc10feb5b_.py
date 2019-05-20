"""empty message

Revision ID: f29dc10feb5b
Revises: 1d1176ae8e6d
Create Date: 2019-05-09 15:07:21.735298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f29dc10feb5b'
down_revision = '1d1176ae8e6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_book_series', 'series', ['series_id'], ['id'], ondelete='RESTRICT')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('fk_book_series', type_='foreignkey')
        batch_op.create_foreign_key(None, 'series', ['series_id'], ['id'])

    # ### end Alembic commands ###
