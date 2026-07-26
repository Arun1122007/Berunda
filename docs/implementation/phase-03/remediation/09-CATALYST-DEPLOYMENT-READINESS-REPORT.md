# Catalyst Deployment Readiness Report

> **Document ID:** BERUNDA-REMEDIATION-009  
> **Status:** READY  

---

## 1. Deployment Contract

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `CATALYST_PROJECT_ID` | Yes | `""` | Catalyst project identifier |
| `CATALYST_API_KEY` | Yes | `""` | Catalyst API authentication |
| `CATALYST_FUNCTION_BASE` | No | Auto-derived from project ID | AppSail function base URL |
| `X_ZOHO_CATALYST_LISTEN_PORT` | No | — | Auto-detection for Catalyst environment |
| `USE_CATALYST` | No | `"false"` | Force Catalyst mode in non-Catalyst env |

### Repository Factory Selection

The `EnvironmentRepositoryFactory` in `src/repositories/factory.py` automatically selects:
- **Catalyst adapters** when in Zoho Catalyst runtime (detected via `X_ZOHO_CATALYST_LISTEN_PORT` or `USE_CATALYST=true`)
- **SQLite adapters** for local development

## 2. AI Provider Readiness

| Feature | Status |
|---------|--------|
| Retry policy | `tenacity` with exponential backoff (3 attempts) |
| Correlation IDs | `X-Correlation-ID` per request |
| Error mapping | `_map_error()` → `AIServiceError` |
| Health check | `GET /api/v1/health` via `health_check()` |
| Timeout | Configurable `request_timeout` (default 30s) |
| Embedding | `POST /api/v1/embed` with retry |

## 3. Vector Store Readiness

| Environment | Store Type | Notes |
|-------------|------------|-------|
| Development | `InMemoryVectorStore` | Cosine similarity via sklearn |
| Self-hosted | `RedisVectorStore` | Redis brute-force scan fallback |
| Catalyst | `CatalystVectorStore` | Placeholder — requires Catalyst AI Search API contract |

## 4. Storage Readiness

| Environment | Storage Backend | Notes |
|-------------|----------------|-------|
| Development | `LocalFileStorage` | Writes to `data/uploads/` |
| Catalyst | Catalyst Filestore | Via `FileStorage` protocol |

## 5. Migration Readiness

Alembic migrations are verified linear (001→007) with `alembic check` confirming head is current.
