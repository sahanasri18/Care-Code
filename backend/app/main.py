"""CareCode API application factory."""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import admin, analytics, auth, hospitals, public, qr, users
from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("carecode")

settings = get_settings()
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


def _create_tables_and_seed() -> None:
    if settings.environment != "production":
        Base.metadata.create_all(bind=engine)
    from app.services.hospital_seed import seed_hospitals

    with SessionLocal() as db:
        seeded = seed_hospitals(db)
        if seeded:
            logger.info("Seeded %d hospitals", seeded)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _create_tables_and_seed()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Emergency medical identification platform — Scan. Care. Save Lives.",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.frontend_url.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}


api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(qr.router, prefix=api_prefix)
app.include_router(public.router, prefix=api_prefix)
app.include_router(hospitals.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)


# --------------------------------------------------------------------------
# Serve the built React SPA (production). API routes take precedence.
# --------------------------------------------------------------------------
if FRONTEND_DIST.is_dir():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str):
        file = FRONTEND_DIST / full_path
        if full_path and file.is_file():
            return FileResponse(file)
        index = FRONTEND_DIST / "index.html"
        if index.is_file():
            return FileResponse(index)
        return JSONResponse(status_code=404, content={"detail": "Not found"})
