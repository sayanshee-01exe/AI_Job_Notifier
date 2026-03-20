"""
Application configuration loaded from environment variables.
Uses pydantic-settings for type-safe configuration.
"""

from pathlib import Path

from pydantic_settings import BaseSettings
from functools import lru_cache

# Resolve .env path relative to this file (backend/.env)
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # ── Database ──────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://shee_sayan@localhost:5432/ai_job_notifier"

    # ── JWT ───────────────────────────────────────────────
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── AI APIs ───────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # ── SMTP ──────────────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    NOTIFICATION_FROM_EMAIL: str = ""

    # ── App ───────────────────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MATCH_SCORE_THRESHOLD: float = 0.7
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = {
        "env_file": str(_ENV_FILE),
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
