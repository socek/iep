"""empty message

Revision ID: 4fef43733470
Revises: 4c296cf8919d
Create Date: 2019-06-30 20:24:40.350783

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4fef43733470'
down_revision = '4c296cf8919d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guests',
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('convention_uid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('kind', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['convention_uid'], ['conventions.uid'], name=op.f('fk_guests_convention_uid_conventions')),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_guests'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guests')
    # ### end Alembic commands ###
