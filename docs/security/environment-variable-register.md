# Environment Variable Register

**Document ID:** BERUNDA-SEC-ENV-001 | **Version:** 2.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-24

---

## Variable Matrix

| Variable | Required | Environment | Description | Safe Default | Secret | Source(s) |
|---|---|---|---|---|---|---|
| `APP_ENV` | No | All | Runtime environment (development/test/staging/production) | `development` | No | `src/shared/config/`, `src/main.py` |
| `LOG_LEVEL` | No | All | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` | No | `src/shared/logging/`, `src/database.py` |
| `HOST` | No | All | Server bind address | `0.0.0.0` | No | `src/shared/config/` |
| `PORT` | No | All | Server port | `8000` | No | `src/shared/config/` |
| `DATABASE_URL` | **Yes** | Production | Database connection string (SQLite for dev, PostgreSQL for prod) | `sqlite+aiosqlite:///./berunda.db` | **Yes** | `src/database.py`, `src/alembic/env.py` |
| `DB_POOL_SIZE` | No | All | Database connection pool size | `5` | No | `src/database.py` |
| `DB_MAX_OVERFLOW` | No | All | Max overflow connections | `10` | No | `src/database.py` |
| `JWT_SECRET` | **Yes** | All | JWT signing secret (min 32 chars; use `secrets.token_hex(32)`) | `dev-secret-change-in-production` | **Yes** | `src/middleware/auth.py` |
| `ACCESS_TOKEN_EXPIRY_MINUTES` | No | All | JWT access token lifetime in minutes | `60` | No | `src/services/auth_service.py` |
| `REFRESH_TOKEN_EXPIRY_DAYS` | No | All | JWT refresh token lifetime in days | `7` | No | `src/services/auth_service.py` |
| `CELERY_BROKER_URL` | Conditional | Production | Celery message broker URL | `redis://localhost:6379/0` | **Yes** | `src/worker.py` |
| `CELERY_RESULT_BACKEND` | Conditional | Production | Celery result backend URL | `redis://localhost:6379/0` | **Yes** | `src/worker.py` |
| `OPENAI_API_KEY` | **Yes** | Production | OpenAI API key for embeddings | (empty) | **Yes** | `src/ai/providers/openai.py` |
| `OPENAI_BASE_URL` | No | All | OpenAI API base URL | `https://api.openai.com/v1` | No | `src/ai/providers/openai.py` |
| `GROQ_API_KEY` | No | All | Groq API key (optional alternative provider) | (empty) | **Yes** | `src/ai/providers/groq.py` |
| `CATALYST_PROJECT_ID` | No | All | Zoho Catalyst project ID | (empty) | **Yes** | `src/ai/providers/catalyst.py` |
| `CATALYST_API_KEY` | No | All | Zoho Catalyst API key | (empty) | **Yes** | `src/ai/providers/catalyst.py` |
| `NEO4J_URI` | No | All | Neo4j connection URI (optional — falls back to NetworkX) | (empty) | No | `src/services/neo4j_service.py` |
| `NEO4J_USER` | No | All | Neo4j username | `neo4j` | No | `src/services/neo4j_service.py` |
| `NEO4J_PASSWORD` | No | All | Neo4j password | (empty) | **Yes** | `src/services/neo4j_service.py` |
| `TEST_DATABASE_URL` | No | Test | Test database URL override | (empty) | No | `tests/integration/conftest.py` |
| `TEST_CACHE_URL` | No | Test | Test cache URL | `redis://localhost:6379/0` | No | `tests/integration/conftest.py` |
| `AUTH_JWT_SECRET` | No | Test | Test JWT secret override | `test-secret` | **Yes** | `tests/conftest.py` |
| `INITIAL_ADMIN_PASSWORD` | No | Migration | Initial admin password for DB seed | `admin123` | **Yes** | `alembic/versions/006_seed_users.py` |
| `INITIAL_ANALYST_PASSWORD` | No | Migration | Initial analyst password for DB seed | `analyst123` | **Yes** | `alembic/versions/006_seed_users.py` |
| `VITE_API_BASE_URL` | No | Frontend | Frontend API base URL | `/api/v1` | No | `apps/web/src/services/api-client.ts` |
| `VITE_API_URL` | No | Frontend | Frontend API URL (Docker build) | `http://localhost:8000` | No | `apps/web/src/services/api-client.ts` |

---

## Configuration Sources

Variables are loaded in the following order (later overrides earlier):

1. **`src/config.py`** — Pydantic `BaseSettings` with typed defaults, auto-loads `.env` via `python-dotenv`
2. **Config files** — `config/base.yaml` + environment-specific override (loaded by `src/shared/config/__init__.py`)
3. **Environment variables** — System/container environment override all file-based config
4. **Catalyst console** — Production secrets managed in Catalyst UI (AppSail injection)

---

## Important Notes

1. **Secrets never logged**: The configuration loader must redact secret values in debug output
2. **`.env.example` is safe**: All example values are obviously fake placeholders
3. **Typed validation available**: `src/config.py` uses Pydantic `BaseSettings` — preferred over raw `os.environ.get()`
4. **Weak defaults warned**: `JWT_SECRET` triggers a runtime `UserWarning` if set to any known placeholder
5. **Production requires explicit secrets**: `DATABASE_URL`, `JWT_SECRET`, `OPENAI_API_KEY`, and Celery URLs must be set for production; `docker-compose.prod.yml` fails fast if `DB_PASSWORD`, `REDIS_PASSWORD`, or `JWT_SECRET` are missing
6. **Neo4j is optional**: Falls back to NetworkX/PostgreSQL when not configured
7. **Catalyst credentials are not needed for local dev**: The FastAPI bootstrap runs without Catalyst
