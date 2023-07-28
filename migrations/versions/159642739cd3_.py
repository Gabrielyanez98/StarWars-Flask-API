"""empty message

Revision ID: 159642739cd3
Revises: 561a37d1f348
Create Date: 2023-07-28 09:52:25.259534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '159642739cd3'
down_revision = '561a37d1f348'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planets_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('characters_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'planets', ['planets_id'], ['id'])
        batch_op.create_foreign_key(None, 'characters', ['characters_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('characters_id')
        batch_op.drop_column('planets_id')

    # ### end Alembic commands ###