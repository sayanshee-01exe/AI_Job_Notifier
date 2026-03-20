"""
AI Job Notifier — FastAPI Application Entry Point.

Production-ready backend for an AI-powered job matching platform.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import get_settings
from backend.core.database import init_db, close_db
from backend.core.exceptions import register_exception_handlers
from backend.core.logging_middleware import LoggingMiddleware
from backend.routes import auth, resume, jobs, recommendations

# ── Logging Setup ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ai_job_notifier")

settings = get_settings()


# ── Lifespan ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 Starting AI Job Notifier API")
    await init_db()
    logger.info("✔  Database initialized")

    from backend.core.database import async_session_factory
    from backend.services.job_service import get_all_jobs_raw
    from backend.vectorstore.store import get_vector_store
    
    logger.info("Loading semantic vector store...")
    async with async_session_factory() as db:
        jobs = await get_all_jobs_raw(db)
        if jobs:
            store = get_vector_store()
            store.populate_from_jobs(jobs)
    logger.info("✔  Vector store populated")

    yield
    await close_db()
    logger.info("🛑 Shutting down AI Job Notifier API")


# ── App ───────────────────────────────────────────────────
app = FastAPI(
    title="AI Job Notifier",
    description="AI-powered job matching platform with resume parsing, "
                "semantic search, and personalized recommendations.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# ── Exception Handlers ───────────────────────────────────
register_exception_handlers(app)

# ── Routes ────────────────────────────────────────────────
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(resume.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)
app.include_router(recommendations.router, prefix=API_PREFIX)


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Job Notifier"}
