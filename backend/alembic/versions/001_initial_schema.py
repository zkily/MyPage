"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_admin_users_username", "admin_users", ["username"])

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("title_ja", sa.String(length=255), nullable=False),
        sa.Column("title_zh", sa.String(length=255), nullable=False),
        sa.Column("title_en", sa.String(length=255), nullable=False),
        sa.Column("desc_ja", sa.Text(), nullable=False),
        sa.Column("desc_zh", sa.Text(), nullable=False),
        sa.Column("desc_en", sa.Text(), nullable=False),
        sa.Column("cover_url", sa.String(length=512), nullable=False),
        sa.Column("tech_stack", mysql.JSON(), nullable=False),
        sa.Column("demo_url", sa.String(length=512), nullable=True),
        sa.Column("repo_url", sa.String(length=512), nullable=True),
        sa.Column("size", sa.Enum("small", "medium", "large", "featured", name="projectsize"), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_projects_slug", "projects", ["slug"])

    op.create_table(
        "knowledge_articles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("title_ja", sa.String(length=255), nullable=False),
        sa.Column("title_zh", sa.String(length=255), nullable=False),
        sa.Column("title_en", sa.String(length=255), nullable=False),
        sa.Column("summary_ja", sa.Text(), nullable=False),
        sa.Column("summary_zh", sa.Text(), nullable=False),
        sa.Column("summary_en", sa.Text(), nullable=False),
        sa.Column("content_ja", sa.Text(), nullable=False),
        sa.Column("content_zh", sa.Text(), nullable=False),
        sa.Column("content_en", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("tags", mysql.JSON(), nullable=False),
        sa.Column("cover_url", sa.String(length=512), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_knowledge_articles_slug", "knowledge_articles", ["slug"])


def downgrade() -> None:
    op.drop_index("ix_knowledge_articles_slug", table_name="knowledge_articles")
    op.drop_table("knowledge_articles")
    op.drop_index("ix_projects_slug", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_admin_users_username", table_name="admin_users")
    op.drop_table("admin_users")
