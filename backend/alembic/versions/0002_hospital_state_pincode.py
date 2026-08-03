"""add state and pincode to hospitals

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-03 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("hospitals", sa.Column("state", sa.String(length=50), nullable=False, server_default="Unknown"))
    op.add_column("hospitals", sa.Column("pincode", sa.String(length=10), nullable=True))
    op.create_index(op.f("ix_hospitals_state"), "hospitals", ["state"])


def downgrade() -> None:
    op.drop_index(op.f("ix_hospitals_state"), table_name="hospitals")
    op.drop_column("hospitals", "pincode")
    op.drop_column("hospitals", "state")
