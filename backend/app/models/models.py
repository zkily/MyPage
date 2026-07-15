import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProjectSize(str, enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"
    featured = "featured"


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    title_ja: Mapped[str] = mapped_column(String(255), nullable=False)
    title_zh: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    title_en: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    desc_ja: Mapped[str] = mapped_column(Text, nullable=False, default="")
    desc_zh: Mapped[str] = mapped_column(Text, nullable=False, default="")
    desc_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cover_url: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    tech_stack: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    demo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    repo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    size: Mapped[ProjectSize] = mapped_column(
        Enum(ProjectSize), nullable=False, default=ProjectSize.medium
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    title_ja: Mapped[str] = mapped_column(String(255), nullable=False)
    title_zh: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    title_en: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    summary_ja: Mapped[str] = mapped_column(Text, nullable=False, default="")
    summary_zh: Mapped[str] = mapped_column(Text, nullable=False, default="")
    summary_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_ja: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_zh: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_en: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    cover_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
