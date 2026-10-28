"""Enable PostGIS without creating domain tables.

Revision ID: 0001
Revises: None
"""
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    # PostGIS may be shared by other schemas. Never drop extensions or dependent user data.
    pass
