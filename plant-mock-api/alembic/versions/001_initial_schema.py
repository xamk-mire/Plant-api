"""Initial schema for plants, plant_care, api_keys

Revision ID: 001
Revises:
Create Date: 2025-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "plants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scientific_name", sa.String(255), nullable=False),
        sa.Column("common_name", sa.String(255), nullable=False),
        sa.Column("family", sa.String(100), nullable=False),
        sa.Column("genus", sa.String(100), nullable=False),
        sa.Column("species", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("native_region", sa.String(255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plants_scientific_name", "plants", ["scientific_name"])
    op.create_index("ix_plants_common_name", "plants", ["common_name"])
    op.create_index("ix_plants_family", "plants", ["family"])

    op.create_table(
        "plant_care",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("watering_frequency", sa.String(100), nullable=True),
        sa.Column("light_requirement", sa.String(100), nullable=True),
        sa.Column("humidity_min", sa.Integer(), nullable=True),
        sa.Column("humidity_max", sa.Integer(), nullable=True),
        sa.Column("temp_min_c", sa.Integer(), nullable=True),
        sa.Column("temp_max_c", sa.Integer(), nullable=True),
        sa.Column("soil_type", sa.String(255), nullable=True),
        sa.Column("fertilizing", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "api_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("key_hash", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_api_keys_key_hash", "api_keys", ["key_hash"], unique=True)


def downgrade() -> None:
    op.drop_table("api_keys")
    op.drop_table("plant_care")
    op.drop_table("plants")
