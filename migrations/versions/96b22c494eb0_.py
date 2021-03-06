"""empty message

Revision ID: 96b22c494eb0
Revises: d54327ccd77f
Create Date: 2021-05-29 17:15:53.969400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96b22c494eb0'
down_revision = 'd54327ccd77f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'contact', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contact', type_='unique')
    # ### end Alembic commands ###
