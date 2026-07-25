"""Typed configuration via Pydantic Settings — single source of truth for all env vars.

Usage:
    from src.config import settings
    settings.JWT_SECRET      # raises if missing in production
    settings.DATABASE_URL    # defaults to SQLite in development
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────
    APP_ENV: str = Field(default="development", alias="APP_ENV")
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")
    HOST: str = Field(default="0.0.0.0", alias="HOST")
    PORT: int = Field(default=8000, alias="PORT")
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:8080",
        alias="CORS_ORIGINS",
    )

    # ── Database ───────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./berunda.db",
        alias="DATABASE_URL",
    )
    DB_POOL_SIZE: int = Field(default=5, alias="DB_POOL_SIZE", ge=1)
    DB_MAX_OVERFLOW: int = Field(default=10, alias="DB_MAX_OVERFLOW", ge=0)
    DATABASE_ECHO: bool = Field(default=False, alias="DATABASE_ECHO")

    # ── Auth & JWT ─────────────────────────────────────────────
    JWT_SECRET: str = Field(
        default="dev-secret-change-in-production",
        alias="JWT_SECRET",
        min_length=16,
    )
    ACCESS_TOKEN_EXPIRY_MINUTES: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRY_MINUTES", ge=1)
    REFRESH_TOKEN_EXPIRY_DAYS: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRY_DAYS", ge=1)

    # ── Celery / Background Tasks ──────────────────────────────
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        alias="CELERY_BROKER_URL",
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        alias="CELERY_RESULT_BACKEND",
    )

    # ── Redis Cache ────────────────────────────────────────────
    REDIS_URL: str = Field(default="redis://localhost:6379/1", alias="REDIS_URL")
    CACHE_TTL_SECONDS: int = Field(default=300, alias="CACHE_TTL_SECONDS", ge=0)

    # ── AI Providers ───────────────────────────────────────────
    LLM_PROVIDER: str = Field(default="", alias="LLM_PROVIDER")
    OPENAI_API_KEY: str = Field(default="", alias="OPENAI_API_KEY")
    OPENAI_BASE_URL: str = Field(
        default="https://api.openai.com/v1",
        alias="OPENAI_BASE_URL",
    )
    GROQ_API_KEY: str = Field(default="", alias="GROQ_API_KEY")
    CATALYST_PROJECT_ID: str = Field(default="", alias="CATALYST_PROJECT_ID")
    CATALYST_API_KEY: str = Field(default="", alias="CATALYST_API_KEY")

    # ── AI Retry Settings ──────────────────────────────────────
    AI_MAX_RETRIES: int = Field(default=3, alias="AI_MAX_RETRIES", ge=0)
    AI_RETRY_DELAY: float = Field(default=2.0, alias="AI_RETRY_DELAY", ge=0)

    # ── Neo4j Graph Database ───────────────────────────────────
    NEO4J_URI: str = Field(default="", alias="NEO4J_URI")
    NEO4J_USER: str = Field(default="neo4j", alias="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(default="", alias="NEO4J_PASSWORD")

    # ── Testing ────────────────────────────────────────────────
    TEST_DATABASE_URL: str = Field(default="", alias="TEST_DATABASE_URL")
    TEST_CACHE_URL: str = Field(
        default="redis://localhost:6379/0",
        alias="TEST_CACHE_URL",
    )
    AUTH_JWT_SECRET: str = Field(
        default="test-secret-not-for-production",
        alias="AUTH_JWT_SECRET",
    )

    # ── Database Seed / Migrations ─────────────────────────────
    INITIAL_ADMIN_PASSWORD: str = Field(
        default="",
        alias="INITIAL_ADMIN_PASSWORD",
    )
    INITIAL_ANALYST_PASSWORD: str = Field(
        default="",
        alias="INITIAL_ANALYST_PASSWORD",
    )

    # ── Frontend (Vite) ────────────────────────────────────────
    VITE_API_BASE_URL: str = Field(default="/api/v1", alias="VITE_API_BASE_URL")
    VITE_API_URL: str = Field(default="http://localhost:8000", alias="VITE_API_URL")

    @field_validator("JWT_SECRET")
    @classmethod
    def _check_jwt_secret(cls, v: str) -> str:
        if v in (
            "dev-secret-change-in-production",
            "replace-with-a-random-64-hex-char-string",
            "replace_this_with_a_secure_random_string_in_production",
        ):
            import warnings

            warnings.warn(
                "JWT_SECRET is set to a known weak default. "
                "Generate a strong secret: python -c 'import secrets; print(secrets.token_hex(32))'",  # noqa: E501
                stacklevel=2,
            )
        return v

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def _check_openai_key(cls, v: str, info) -> str:
        if not v and info.data.get("APP_ENV") == "production":
            raise ValueError("OPENAI_API_KEY is required when APP_ENV=production")
        return v

    @field_validator("INITIAL_ADMIN_PASSWORD", "INITIAL_ANALYST_PASSWORD")
    @classmethod
    def _warn_default_seed_passwords(cls, v: str, info) -> str:
        defaults = {"admin123", "analyst123"}
        if v in defaults and info.data.get("APP_ENV") == "production":
            import warnings

            warnings.warn(
                f"{info.field_name} is set to a known weak default. "
                "Override with a strong password via environment variable.",
                stacklevel=2,
            )
        return v

    @field_validator("INITIAL_ADMIN_PASSWORD", "INITIAL_ANALYST_PASSWORD")
    @classmethod
    def _generate_password_if_empty(cls, v: str) -> str:
        if not v:
            import secrets
            import warnings

            generated = secrets.token_urlsafe(16)
            warnings.warn(
                f"Password not set via env var — generated random password: {generated}. "
                "Set INITIAL_ADMIN_PASSWORD / INITIAL_ANALYST_PASSWORD in .env "
                "for a known credential.",
                stacklevel=2,
            )
            return generated
        return v

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_testing(self) -> bool:
        return self.APP_ENV in ("test", "testing")


settings = Settings()
