"""empty message

Revision ID: ecfc7daa95bb
Revises: f840c1fabbae
Create Date: 2019-06-10 18:18:55.670779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecfc7daa95bb'
down_revision = 'f840c1fabbae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('panels', sa.Column('minutes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('panels', 'minutes')
    # ### end Alembic commands ###