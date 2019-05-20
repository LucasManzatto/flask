"""empty message

Revision ID: b70c4ff386cc
Revises: f15351c13059
Create Date: 2019-05-14 15:40:34.461712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70c4ff386cc'
down_revision = 'f15351c13059'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author_series',
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('series_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('author_series')
    # ### end Alembic commands ###