"""empty message

Revision ID: df47b9cf4b14
Revises: f7c74eaefdce
Create Date: 2016-09-28 23:41:20.907609

"""

# revision identifiers, used by Alembic.
revision = 'df47b9cf4b14'
down_revision = 'f7c74eaefdce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('followers', sa.Column('id', sa.Integer(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('followers', 'id')
    ### end Alembic commands ###
