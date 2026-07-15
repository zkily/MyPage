from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LangCode = Literal["ja", "zh", "en"]
ProjectSizeType = Literal["small", "medium", "large", "featured"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class ProjectBase(BaseModel):
    slug: str
    title_ja: str
    title_zh: str = ""
    title_en: str = ""
    desc_ja: str = ""
    desc_zh: str = ""
    desc_en: str = ""
    cover_url: str = ""
    tech_stack: list[str] = Field(default_factory=list)
    demo_url: str | None = None
    repo_url: str | None = None
    size: ProjectSizeType = "medium"
    sort_order: int = 0
    is_published: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    slug: str | None = None
    title_ja: str | None = None
    title_zh: str | None = None
    title_en: str | None = None
    desc_ja: str | None = None
    desc_zh: str | None = None
    desc_en: str | None = None
    cover_url: str | None = None
    tech_stack: list[str] | None = None
    demo_url: str | None = None
    repo_url: str | None = None
    size: ProjectSizeType | None = None
    sort_order: int | None = None
    is_published: bool | None = None


class ProjectAdminResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ProjectPublicResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    cover_url: str
    tech_stack: list[str]
    demo_url: str | None
    repo_url: str | None
    size: ProjectSizeType
    sort_order: int
    created_at: datetime


class KnowledgeBase(BaseModel):
    slug: str
    title_ja: str
    title_zh: str = ""
    title_en: str = ""
    summary_ja: str = ""
    summary_zh: str = ""
    summary_en: str = ""
    content_ja: str = ""
    content_zh: str = ""
    content_en: str = ""
    category: str = ""
    tags: list[str] = Field(default_factory=list)
    cover_url: str | None = None
    is_published: bool = False
    published_at: datetime | None = None


class KnowledgeCreate(KnowledgeBase):
    pass


class KnowledgeUpdate(BaseModel):
    slug: str | None = None
    title_ja: str | None = None
    title_zh: str | None = None
    title_en: str | None = None
    summary_ja: str | None = None
    summary_zh: str | None = None
    summary_en: str | None = None
    content_ja: str | None = None
    content_zh: str | None = None
    content_en: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    cover_url: str | None = None
    is_published: bool | None = None
    published_at: datetime | None = None


class KnowledgeAdminResponse(KnowledgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class KnowledgePublicResponse(BaseModel):
    id: int
    slug: str
    title: str
    summary: str
    content: str
    category: str
    tags: list[str]
    cover_url: str | None
    published_at: datetime | None
    created_at: datetime


class KnowledgeListItem(BaseModel):
    id: int
    slug: str
    title: str
    summary: str
    category: str
    tags: list[str]
    cover_url: str | None
    published_at: datetime | None
    created_at: datetime


class UploadResponse(BaseModel):
    url: str


class DashboardStats(BaseModel):
    projects_total: int
    projects_published: int
    knowledge_total: int
    knowledge_published: int
