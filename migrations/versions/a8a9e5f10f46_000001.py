"""000001

Revision ID: a8a9e5f10f46
Revises:
Create Date: 2023-06-22 16:19:09.212035

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Enum, text


# revision identifiers, used by Alembic.
revision = 'a8a9e5f10f46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create Enum type
    gender_type = Enum('F', 'M', 'O', name='gendertype', create_type=False)
    gender_type.create(op.get_bind(), checkfirst=False)

    # Add column with Enum type
    op.add_column('user', sa.Column('gender', gender_type, nullable=True, server_default=text("'O'::gendertype")))


def downgrade():
    op.drop_column('user', 'gender')
    gender_type = Enum('F', 'M', 'O', name='gendertype', create_type=False)
    gender_type.drop(op.get_bind(), checkfirst=False)
