from app.models.models import KnowledgeArticle, Project
from app.schemas.schemas import (
    KnowledgeListItem,
    KnowledgePublicResponse,
    LangCode,
    ProjectPublicResponse,
)


def _pick_lang(ja: str, zh: str, en: str, lang: LangCode) -> str:
    if lang == "zh" and zh:
        return zh
    if lang == "en" and en:
        return en
    return ja


def project_to_public(project: Project, lang: LangCode) -> ProjectPublicResponse:
    return ProjectPublicResponse(
        id=project.id,
        slug=project.slug,
        title=_pick_lang(project.title_ja, project.title_zh, project.title_en, lang),
        description=_pick_lang(project.desc_ja, project.desc_zh, project.desc_en, lang),
        cover_url=project.cover_url,
        tech_stack=project.tech_stack or [],
        demo_url=project.demo_url,
        repo_url=project.repo_url,
        size=project.size.value,
        sort_order=project.sort_order,
        created_at=project.created_at,
    )


def knowledge_to_public(article: KnowledgeArticle, lang: LangCode) -> KnowledgePublicResponse:
    return KnowledgePublicResponse(
        id=article.id,
        slug=article.slug,
        title=_pick_lang(article.title_ja, article.title_zh, article.title_en, lang),
        summary=_pick_lang(article.summary_ja, article.summary_zh, article.summary_en, lang),
        content=_pick_lang(article.content_ja, article.content_zh, article.content_en, lang),
        category=article.category,
        tags=article.tags or [],
        cover_url=article.cover_url,
        published_at=article.published_at,
        created_at=article.created_at,
    )


def knowledge_to_list_item(article: KnowledgeArticle, lang: LangCode) -> KnowledgeListItem:
    return KnowledgeListItem(
        id=article.id,
        slug=article.slug,
        title=_pick_lang(article.title_ja, article.title_zh, article.title_en, lang),
        summary=_pick_lang(article.summary_ja, article.summary_zh, article.summary_en, lang),
        category=article.category,
        tags=article.tags or [],
        cover_url=article.cover_url,
        published_at=article.published_at,
        created_at=article.created_at,
    )
