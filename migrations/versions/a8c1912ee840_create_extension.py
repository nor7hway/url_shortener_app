"""Create extension

Revision ID: a8c1912ee840
Revises: 
Create Date: 2021-08-27 17:16:06.349537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8c1912ee840'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute('create extension "uuid-ossp"')


def downgrade():
    conn = op.get_bind()
    conn.execute('drop extension "uuid-ossp"')
