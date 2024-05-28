"""retirando o campo numero

Revision ID: 638a7e62f0a6
Revises: 
Create Date: 2024-05-28 13:16:22.119537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '638a7e62f0a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enderecos', schema=None) as batch_op:
        batch_op.drop_column('numero')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enderecos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numero', sa.VARCHAR(length=20), nullable=True))

    # ### end Alembic commands ###
