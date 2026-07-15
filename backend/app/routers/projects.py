from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, Project, ProjectSize
from app.schemas.schemas import (
    LangCode,
    ProjectAdminResponse,
    ProjectCreate,
    ProjectPublicResponse,
    ProjectUpdate,
)
from app.services.i18n import project_to_public

router = APIRouter(tags=["projects"])
admin_router = APIRouter(prefix="/api/admin/projects", tags=["admin-projects"])


@router.get("/api/projects", response_model=list[ProjectPublicResponse])
def list_projects(
    lang: LangCode = Query("ja"),
    db: Session = Depends(get_db),
) -> list[ProjectPublicResponse]:
    projects = (
        db.query(Project)
        .filter(Project.is_published.is_(True))
        .order_by(Project.sort_order.asc(), Project.id.desc())
        .all()
    )
    return [project_to_public(p, lang) for p in projects]


@router.get("/api/projects/{slug}", response_model=ProjectPublicResponse)
def get_project(
    slug: str,
    lang: LangCode = Query("ja"),
    db: Session = Depends(get_db),
) -> ProjectPublicResponse:
    project = (
        db.query(Project)
        .filter(Project.slug == slug, Project.is_published.is_(True))
        .first()
    )
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project_to_public(project, lang)


@admin_router.get("", response_model=list[ProjectAdminResponse])
def admin_list_projects(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> list[ProjectAdminResponse]:
    return (
        db.query(Project)
        .order_by(Project.sort_order.asc(), Project.id.desc())
        .all()
    )


@admin_router.post("", response_model=ProjectAdminResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> ProjectAdminResponse:
    if db.query(Project).filter(Project.slug == payload.slug).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already exists")

    project = Project(**payload.model_dump())
    project.size = ProjectSize(payload.size)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@admin_router.get("/{project_id}", response_model=ProjectAdminResponse)
def get_admin_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> ProjectAdminResponse:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@admin_router.put("/{project_id}", response_model=ProjectAdminResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> ProjectAdminResponse:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    data = payload.model_dump(exclude_unset=True)
    if "slug" in data and data["slug"] != project.slug:
        if db.query(Project).filter(Project.slug == data["slug"]).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already exists")

    if "size" in data and data["size"] is not None:
        data["size"] = ProjectSize(data["size"])

    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@admin_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()
