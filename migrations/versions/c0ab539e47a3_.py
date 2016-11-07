"""empty message

Revision ID: c0ab539e47a3
Revises: None
Create Date: 2016-11-07 20:57:09.647610

"""

## revision identifiers, used by Alembic.
revision = 'c0ab539e47a3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pwreset', sa.Column('has_activated', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pwreset', 'has_activated')
    ### end Alembic commands ###