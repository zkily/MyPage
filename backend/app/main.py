from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine
from app.routers import admin, auth, knowledge, projects
from app.services.seed import seed_database

settings = get_settings()
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(title="MyPage API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(UPLOAD_DIR)), name="static")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(projects.admin_router)
app.include_router(knowledge.router)
app.include_router(knowledge.admin_router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
