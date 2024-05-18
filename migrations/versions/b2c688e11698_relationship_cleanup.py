"""relationship cleanup

Revision ID: b2c688e11698
Revises: a53dceb3313b
Create Date: 2024-05-18 16:05:18.913884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c688e11698'
down_revision = 'a53dceb3313b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('like_count', sa.Integer(), nullable=True))

    with op.batch_alter_table('reply', schema=None) as batch_op:
        batch_op.add_column(sa.Column('like_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reply', schema=None) as batch_op:
        batch_op.drop_column('like_count')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('like_count')

    # ### end Alembic commands ###
