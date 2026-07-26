# Catalyst AI Provider Remediation Report

> **Document ID:** BERUNDA-REMEDIATION-003  
> **Defect:** P3V-BLK-002, P3V-OBS-001  
> **Status:** CLOSED  

---

## 1. Defect Description

- `CatalystProvider` used hardcoded `/functions/llm-chat/execute` and `/functions/llm-embed/execute` endpoints
- No correlation ID propagation or structured error mapping
- Missing `health_check()` method
- Vector store lacked a clean protocol contract

## 2. Remediation

### `catalyst.py` — AppSail Function Contract

| Change | Details |
|--------|---------|
| Endpoints | Changed to `/api/v1/chat` and `/api/v1/embed` per AppSail contract |
| `function_base` | Configurable via `CATALYST_FUNCTION_BASE` environment variable |
| Correlation IDs | `X-Correlation-ID` header on every request |
| Timeout | Configurable `request_timeout` (default 30s) |
| Error mapping | `_map_error()` maps HTTP status codes to `AIServiceError` |
| Retry policy | `tenacity` retry with exponential backoff (3 attempts, 2-30s window) |
| Health check | `health_check()` probes `/api/v1/health` endpoint |
| Pydantic validation | Response parsing uses strict dict access with fallbacks |

### `vector_stores.py` — Vector Store Protocol

| Change | Details |
|--------|---------|
| `VectorStore` protocol | Added a PEP 544 `Protocol` class defining the contract |
| `BaseVectorStore` ABC | Retained as the abstract base for implementation |
| `CatalystVectorStore` | Documented production contract with Catalyst Data Store ZCQL expectations |
| `InMemoryVectorStore` | Unchanged — retained for offline development |
| `RedisVectorStore` | Unchanged — retained for self-hosted production |
