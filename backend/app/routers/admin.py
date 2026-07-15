import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, KnowledgeArticle, Project
from app.schemas.schemas import DashboardStats, UploadResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    _: AdminUser = Depends(get_current_admin),
) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename

    content = await file.read()
    filepath.write_bytes(content)

    return UploadResponse(url=f"/static/{filename}")


@router.get("/stats", response_model=DashboardStats)
def get_stats(
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
) -> DashboardStats:
    projects_total = db.query(Project).count()
    projects_published = db.query(Project).filter(Project.is_published.is_(True)).count()
    knowledge_total = db.query(KnowledgeArticle).count()
    knowledge_published = (
        db.query(KnowledgeArticle).filter(KnowledgeArticle.is_published.is_(True)).count()
    )

    return DashboardStats(
        projects_total=projects_total,
        projects_published=projects_published,
        knowledge_total=knowledge_total,
        knowledge_published=knowledge_published,
    )
