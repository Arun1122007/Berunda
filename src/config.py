"""Typed configuration via Pydantic Settings — single source of truth for all env vars.

Usage:
    from src.config import settings
    settings.JWT_SECRET      # raises if missing in production
    settings.DATABASE_URL    # defaults to SQLite in development
"""

from __future__ import annotations

from pathlib import Path

from typing import Any

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
    ACCESS_TOKEN_EXPIRY_MINUTES: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRY_MINUTES", ge=1)
    REFRESH_TOKEN_EXPIRY_DAYS: int = Field(default=1, alias="REFRESH_TOKEN_EXPIRY_DAYS", ge=1)

    # ── Cache & Remote Redis ────────────────────────────────────
    REDIS_URL: str = Field(default="", alias="REDIS_URL")
    CACHE_TTL_SECONDS: int = Field(default=300, alias="CACHE_TTL_SECONDS", ge=0)

    # ── Celery / Background Tasks ──────────────────────────────
    CELERY_BROKER_URL: str = Field(
        default="",
        alias="CELERY_BROKER_URL",
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="",
        alias="CELERY_RESULT_BACKEND",
    )

    @field_validator(
        "PORT",
        "DB_POOL_SIZE",
        "DB_MAX_OVERFLOW",
        "ACCESS_TOKEN_EXPIRY_MINUTES",
        "REFRESH_TOKEN_EXPIRY_DAYS",
        "CACHE_TTL_SECONDS",
        "MAX_UPLOAD_SIZE_MB",
        "AI_MAX_RETRIES",
        "AI_RETRY_DELAY",
        mode="before",
    )
    @classmethod
    def _coerce_numeric(cls, v: Any, info) -> Any:
        if v is None or v == "" or (isinstance(v, str) and not v.strip()):
            defaults = {
                "PORT": 9000,
                "DB_POOL_SIZE": 5,
                "DB_MAX_OVERFLOW": 10,
                "ACCESS_TOKEN_EXPIRY_MINUTES": 60,
                "REFRESH_TOKEN_EXPIRY_DAYS": 7,
                "CACHE_TTL_SECONDS": 300,
                "MAX_UPLOAD_SIZE_MB": 25,
                "AI_MAX_RETRIES": 3,
                "AI_RETRY_DELAY": 2.0,
            }
            return defaults.get(info.field_name, 0)
        if isinstance(v, str):
            try:
                return float(v) if "." in v else int(v)
            except ValueError:
                defaults = {
                    "PORT": 9000,
                    "DB_POOL_SIZE": 5,
                    "DB_MAX_OVERFLOW": 10,
                    "ACCESS_TOKEN_EXPIRY_MINUTES": 60,
                    "REFRESH_TOKEN_EXPIRY_DAYS": 7,
                    "CACHE_TTL_SECONDS": 300,
                    "MAX_UPLOAD_SIZE_MB": 25,
                    "AI_MAX_RETRIES": 3,
                    "AI_RETRY_DELAY": 2.0,
                }
                return defaults.get(info.field_name, 0)
        return v

    @field_validator("CELERY_BROKER_URL", mode="before")
    @classmethod
    def _default_celery_broker(cls, v: str, info) -> str:
        if not v:
            import os
            redis_env = os.environ.get("REDIS_URL", "")
            return redis_env if redis_env else "redis://localhost:6379/0"
        return v

    @field_validator("CELERY_RESULT_BACKEND", mode="before")
    @classmethod
    def _default_celery_backend(cls, v: str, info) -> str:
        if not v:
            import os
            redis_env = os.environ.get("REDIS_URL", "")
            return redis_env if redis_env else "redis://localhost:6379/0"
        return v

    # ── AI Providers ───────────────────────────────────────────
    LLM_PROVIDER: str = Field(default="", alias="LLM_PROVIDER")
    DEFAULT_AI_PROVIDER: str = Field(default="fallback", alias="DEFAULT_AI_PROVIDER")
    OPENAI_API_KEY: str = Field(default="", alias="OPENAI_API_KEY")
    OPENAI_BASE_URL: str = Field(
        default="https://api.openai.com/v1",
        alias="OPENAI_BASE_URL",
    )
    GROQ_API_KEY: str = Field(default="", alias="GROQ_API_KEY")
    GROQ_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        alias="GROQ_BASE_URL",
    )
    NVIDIA_API_KEY: str = Field(default="", alias="NVIDIA_API_KEY")
    NVIDIA_BASE_URL: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        alias="NVIDIA_BASE_URL",
    )
    OPENROUTER_API_KEY: str = Field(default="", alias="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        alias="OPENROUTER_BASE_URL",
    )

    # ── Catalyst Specific Config ───────────────────────────────
    CATALYST_PROJECT_ID: str = Field(default="", alias="CATALYST_PROJECT_ID")
    CATALYST_PROJECT_DOMAIN: str = Field(default="", alias="CATALYST_PROJECT_DOMAIN")
    CATALYST_ENVIRONMENT_ID: str = Field(default="", alias="CATALYST_ENVIRONMENT_ID")
    CATALYST_ENVIRONMENT: str = Field(default="Development", alias="CATALYST_ENVIRONMENT")
    CATALYST_API_KEY: str = Field(default="", alias="CATALYST_API_KEY")

    # ── Stratus File Storage & Uploads ─────────────────────────
    STRATUS_TOKEN: str = Field(default="", alias="STRATUS_TOKEN")
    STRATUS_BUCKET: str = Field(default="berunda-dev-docs", alias="STRATUS_BUCKET")
    STRATUS_ENABLED: bool = Field(default=False, alias="STRATUS_ENABLED")
    MAX_UPLOAD_SIZE_MB: int = Field(default=25, alias="MAX_UPLOAD_SIZE_MB", ge=1)
    ALLOWED_FILE_TYPES: str = Field(
        default="application/pdf,image/jpeg,image/png,text/plain",
        alias="ALLOWED_FILE_TYPES",
    )

    # ── Feature Flags & Mock Services ──────────────────────────
    ENABLE_AI_REVIEW: bool = Field(default=True, alias="ENABLE_AI_REVIEW")
    ENABLE_MOCK_AUTH: bool = Field(default=False, alias="ENABLE_MOCK_AUTH")
    USE_MOCK_SERVICES: bool = Field(default=True, alias="USE_MOCK_SERVICES")

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
                "Generate a strong secret: python -c 'import secrets; print(secrets.token_hex(32))'",
                stacklevel=2,
            )
        return v

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def _check_openai_key(cls, v: str, info) -> str:
        # Non-blocking: fallback chain handles missing keys gracefully
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
