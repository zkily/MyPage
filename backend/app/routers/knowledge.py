from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, KnowledgeArticle
from app.schemas.schemas import (
    KnowledgeAdminResponse,
    KnowledgeCreate,
    KnowledgeListItem,
    KnowledgePublicResponse,
    KnowledgeUpdate,
    LangCode,
)
from app.services.i18n import knowledge_to_list_item, knowledge_to_public

router = APIRouter(tags=["knowledge"])
admin_router = APIRouter(prefix="/api/admin/knowledge", tags=["admin-knowledge"])


@router.get("/api/knowledge", response_model=list[KnowledgeListItem])
def list_knowledge(
    lang: LangCode = Query("ja"),
    db: Session = Depends(get_db),
) -> list[KnowledgeListItem]:
    articles = (
        db.query(KnowledgeArticle)
        .filter(KnowledgeArticle.is_published.is_(True))
        .order_by(KnowledgeArticle.published_at.desc(), KnowledgeArticle.id.desc())
        .all()
    )
    return [knowledge_to_list_item(a, lang) for a in articles]


@router.get("/api/knowledge/{slug}", response_model=KnowledgePublicResponse)
def get_knowledge(
    slug: str,
    lang: LangCode = Query("ja"),
    db: Session = Depends(get_db),
) -> KnowledgePublicResponse:
    article = (
        db.query(KnowledgeArticle)
        .filter(KnowledgeArticle.slug == slug, KnowledgeArticle.is_published.is_(True))
        .first()
    )
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return knowledge_to_public(article, lang)


@admin_router.get("", response_model=list[KnowledgeAdminResponse])
def admin_list_knowledge(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> list[KnowledgeAdminResponse]:
    return (
        db.query(KnowledgeArticle)
        .order_by(KnowledgeArticle.published_at.desc(), KnowledgeArticle.id.desc())
        .all()
    )


@admin_router.post("", response_model=KnowledgeAdminResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge(
    payload: KnowledgeCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> KnowledgeAdminResponse:
    if db.query(KnowledgeArticle).filter(KnowledgeArticle.slug == payload.slug).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already exists")

    article = KnowledgeArticle(**payload.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@admin_router.get("/{article_id}", response_model=KnowledgeAdminResponse)
def get_admin_knowledge(
    article_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> KnowledgeAdminResponse:
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article


@admin_router.put("/{article_id}", response_model=KnowledgeAdminResponse)
def update_knowledge(
    article_id: int,
    payload: KnowledgeUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> KnowledgeAdminResponse:
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    data = payload.model_dump(exclude_unset=True)
    if "slug" in data and data["slug"] != article.slug:
        if db.query(KnowledgeArticle).filter(KnowledgeArticle.slug == data["slug"]).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already exists")

    for key, value in data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article


@admin_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(
    article_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> None:
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    db.delete(article)
    db.commit()
