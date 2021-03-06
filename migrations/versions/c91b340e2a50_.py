"""empty message

Revision ID: c91b340e2a50
Revises: 4ad161f8b474
Create Date: 2019-08-19 16:35:13.384596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c91b340e2a50'
down_revision = '4ad161f8b474'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'is_deleted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
