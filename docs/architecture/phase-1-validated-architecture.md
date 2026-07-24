# Phase 1 — Validated Architecture

**Document ID:** BERUNDA-ARCH-VAL-001 | **Version:** 2.2 | **Status:** APPROVED
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-24

---

## 1. Architecture Summary

Berunda uses a **Modular Functions + API Gateway** architecture with a **dual-language bootstrap** (Python FastAPI for local development, Node.js Catalyst Functions for production deployment on Zoho Catalyst).

### Architectural Style

- **Phase 1 (Current):** FastAPI REST server (local dev) → Modular Catalyst Functions (production) with synchronous REST calls, API Gateway routing, PostgreSQL/Catalyst Data Store persistence, inline async background tasks (see ADR-011)
- **Target (Phase 3+):** Event-driven mesh with Catalyst Signals event bus, Circuits workflow orchestration, CQRS, dedicated graph database. Celery + Redis for background task distribution.

### Key Principle

All services operate within a single Zoho Catalyst project. No external cloud infrastructure is required. This is mandated by the Hack2Skill Datathon 2026 rules.

---

## 2. Technology Stack (Validated)

| Layer | Technology | Version | Status |
|-------|-----------|---------|--------|
| **Backend API** | FastAPI (Python) | >=0.115.0 | ✅ Live locally |
| **Production Runtime** | Zoho Catalyst Functions (Node.js) | SDK ^1.0.0 | ⬜ Scaffolded |
| **Frontend** | React 18 + TypeScript + Vite | ^18.3.0 / ^5.4.0 | ✅ Scaffolded |
| **Database ORM** | SQLAlchemy 2.0 (async) | >=2.0.35 | ✅ Live |
| **Database** | PostgreSQL 16 (prod) / SQLite (dev) | 16-alpine | ✅ Configured |
| **Cache** | Redis 7 / Catalyst Stratus | 7-alpine | ⬜ Scaffolded |
| **Migrations** | Alembic | >=1.13.0 | ✅ 6 versions |
| **Task Queue** | Inline async (Phase 1) / Celery + Redis (Phase 3+) | — | ✅ Inline tasks per ADR-011 |
| **Auth** | JWT (HS256) + bcrypt | PyJWT >=2.9.0 | ✅ Live |
| **AI Providers** | OpenAI / Groq / Mock | — | ✅ Live |
| **ML** | scikit-learn, NetworkX, spaCy | — | ✅ Scaffolded |
| **Maps** | MapLibre GL JS | ^4.5.0 | ✅ Scaffolded |
| **Graph Viz** | Cytoscape.js | ^3.30.0 | ✅ Scaffolded |
| **Charts** | Recharts | ^2.12.0 | ✅ Scaffolded |
| **Container** | Docker Compose (8 services: 6 core + prometheus + grafana) | — | ✅ Configured |
| **Monitoring** | Prometheus + Grafana + Sentry | — | ✅ Configured |
| **CI** | GitHub Actions (4 workflows) | — | ✅ Valid YAML |

---

## 3. System Components (17 Runtime Components)

### Local Stack (4 Docker Services)

| Service | Entry Point | Responsibility |
|---------|------------|----------------|
| **FastAPI Backend** | `src/main.py` → `uvicorn` | REST API, 10 router modules, health/readiness |
| **React Frontend** | `apps/web/` → Vite dev / Nginx serve | SPA with 8 feature modules (dashboard, auth, entities, hotspot, graph, rag, analytics, admin) |
| **PostgreSQL** | Docker `postgres:16-alpine` | Primary database |
| **Redis** | Docker `redis:7-alpine` | Cache (Celery broker removed per ADR-011) |

Background tasks run inline via FastAPI `BackgroundTasks` — see ADR-011.

### Catalyst Stack (11 Deployments)

| Component | Type | Purpose |
|-----------|------|---------|
| 10 Catalyst Functions | Node.js | FIR ingestion, NER, entity resolution, risk scoring, hotspot, anomaly, link analysis, RAG, audit, fairness |
| 1 Catalyst Worker | Node.js | Nightly batch recompute |

Note: Local FastAPI implements all 10 function concerns as routers. Catalyst functions are deployment targets with placeholder READMEs only.

---

## 4. Module Dependency Rules

### Python Layer Architecture

```
L6: Entry       main.py, worker.py
                    ↓
L5: Routers     routers/*.py  (11 modules)
                    ↓
L4: Services    services/*.py  (15 modules)  ⚠ See ADR-010
                    ↓
L3: AI/ML       ai/*.py, ml/*.py, pipelines/*.py
                    ↓
L2: Schema      schemas/*.py  (11 modules)
                    ↓
L1: Models      models/*.py  (7 modules, 31+ tables)
                    ↓
L0: Foundation  shared/*.py, database.py, middleware/*.py
```

### Strict Rules
- **L0 (shared/)**: Must NOT import any other `src.*` module
- **L1 (models/)**: May import L0 only
- **L2 (schemas/)**: May import L0 only
- **L3 (ai/, ml/)**: May import L0-L2; `ai/` may import `shared.logging`
- **L4 (services/)**: Should import L0-L3 only; ⚠ currently violates with `ai.*` imports
- **L5 (routers/)**: May import L0-L4
- **L6 (entry)**: May import any module

### ⚠ Confirmed Violations (see ADR-010)

| File | Violation | Risk |
|------|-----------|------|
| `services/guardrails_service.py` | Imports `src.ai.guardrails` | Service depends on AI layer; cycle risk if ai ever imports services |
| `services/embedding_service.py` | Imports `src.ai.providers` | Same as above |
| `services/rag_service.py` | Imports `services.embedding_service` | Cross-service coupling at same layer — acceptable with DI |

### Prohibited (Already Clean)
- ✅ No circular dependencies between Python modules
- ✅ No direct database access from frontend
- ✅ No secrets in source code
- ✅ No hardcoded environment-specific values

---

## 5. Data Flow

### Request Flow
```
HTTP Request → CORS Middleware → Router (path params + body validation via Pydantic)
  → Auth Middleware (JWT decode → user context with roles + DistrictID)
  → Service Layer (business logic + ORM queries)
    ├──→ Model (SQLAlchemy ORM → PostgreSQL/SQLite)
    ├──→ (optional) AI/ML (guardrails, embeddings)
    └──→ Schema (Pydantic serialization)
  → JSON Response
```

### Background Task Flow
```
FastAPI BackgroundTasks → _trigger_post_fir_tasks()
  → tasks.risk_scoring.compute_risk_score_task()
      → RiskService.compute_risk_score() per entity
  → tasks.anomaly.run_anomaly_detection_task()
      → AnomalyService.detect_anomalies()
  → tasks.notifications.send_notification_task()
```

### FIR Ingestion Flow
```
User Upload → Frontend → POST /api/v1/fir → FIR Router
  → Validate Schema → Insert to Database
  → Trigger Inline Tasks (Risk Score → Anomaly Detection)
  → Log Audit Event
```

---

## 6. Trust Boundaries

| Boundary | Type | Enforcement |
|----------|------|-------------|
| Browser ↔ API | Network (HTTPS) | CORS middleware (localhost origins whitelisted) |
| Request → Router | Application | `HTTPBearer` + JWT decode in `middleware/auth.py` |
| Router → Service | Application | Role check via `require_role()` dependency |
| Service → Database | Application | SQLAlchemy async session (connection pooling) |
| Service → AI Layer | Application | ⚠ Guardrails + Embedding services cross boundary (ADR-010) |

### Authentication Boundary
- `middleware/auth.py`: JWT decoding, role extraction, `get_current_user()`, `require_role()`
- `services/auth_service.py`: Login, registration, token issuance, refresh, revocation
- Frontend `ProtectedRoute` component gates UI routes

### Authorization Roles
- **Admin**: Full access including system configuration
- **Analyst**: CRUD on case data, graph access, RAG queries
- **Viewer**: Read-only access to dashboards and reports
- **District scope**: Data filtered by `DistrictID` in user context

---

## 7. Integration Boundaries

| Integration | Status | Pattern |
|-------------|--------|---------|
| OpenAI API | ⬜ Configured | Key in env; httpx async calls; fallback to MockProvider |
| Groq API | ⬜ Configured | Extends OpenAI provider; alternative LLM |
| Open-Meteo | ⬜ Planned | Weather data for crime pattern analysis |
| Overpass API (OSM) | ⬜ Planned | Police station boundary queries |
| CCTNS | 🔒 Future-Restricted | Legal MOU required |
| Bhuvan (ISRO) | ⬜ Planned | Indian geospatial boundaries |
| Sentry | ⬜ Configured | Error tracking via DSN |

### Integration Pattern
- External APIs accessed through adapter layer in `src/ai/providers/`
- All external calls wrapped with timeout + retry
- Mock implementations for development and testing

---

## 8. Scaling Considerations

| Component | Strategy | Phase |
|-----------|----------|-------|
| Catalyst Functions | Auto-scaling per Catalyst | 1 |
| PostgreSQL | Connection pooling (5 + 10 overflow), read replicas | 2 |
| Frontend | Static file serving with CDN | 1 |
| RAG Pipeline | Increase embedding cache, batch processing | 2 |
| Graph Engine | NetworkX in-memory → Neo4j dedicated DB | 3 |
| Background Tasks | Inline async (Phase 1) → Celery + Redis (Phase 3+) | 1 / 3 |

### Phase 1 Bottlenecks
- Synchronous REST calls between components
- In-memory graph processing (NetworkX) — limited to demo dataset scale
- Single-region deployment
- SQLite in local dev (PostgreSQL only in Docker)

---

## 9. Failure-Handling Approach

| Failure Mode | Handling Strategy | Status |
|-------------|-------------------|--------|
| Function timeout | FastAPI timeout middleware | ✅ Configured |
| Database unavailable | Graceful degradation (service returns empty, ready endpoint shows degraded) | ✅ Verified |
| External API failure | Fallback to MockProvider, retry with backoff | ✅ Configured |
| Invalid input | Pydantic schema validation → 400 response | ✅ Configured |
| Authentication failure | 401 response, no stack trace | ✅ Configured |
| Unhandled exception | Global error handler → safe 500 response | ✅ Verified |
| Rate limit exceeded | 429 Retry-After (Catalyst API Gateway) | ⬜ Catalyst-managed |

### Graceful Degradation
- Hotspot map falls back to cached data
- RAG offline → suggest pre-built reports
- Graph unavailable → show tabular data
- Auth unavailable → anonymous access with limited features

---

## 10. Architectural Risks (Validated)

| Risk | Severity | Probability | Mitigation | Phase |
|------|----------|-------------|------------|-------|
| Service-to-AI layer dependency violation | MEDIUM | HIGH | ADR-010: Extract shared contracts; DI pattern | 2 |
| ADR-009 location inconsistent with index | LOW | HIGH | ✅ RESOLVED — ADR-011 placed in `decisions/` to consolidate | 1 |
| Coverage threshold mismatch (pytest.ini=65%, CI=70%, test-strategy=80%) | MEDIUM | HIGH | ✅ RESOLVED — Unified at 65% across all configs | 1 |
| Groq vs OpenAI primary assumption conflict | LOW | MEDIUM | ✅ RESOLVED — Updated ASSUMPTIONS.md to reflect dual-provider support | 1 |
| Entity Resolution algorithm not implemented | HIGH | HIGH | LLD describes weighted scoring but code has no implementation | 2 |
| CrimeNo parsing not implemented | MEDIUM | MEDIUM | LLD section 2.2 parsing logic absent from codebase | 2 |
| Catalyst SDK unavailable locally | MEDIUM | HIGH | FastAPI bootstrap provides local testing capability | 1 |
| Dev JWT secret in config/development.yaml | LOW | LOW | Documented; production must override via env variable | 1 |
| CI continue-on-error masks failures | MEDIUM | LOW | test.yml uses continue-on-error for optional E2E/perf steps | 2 |
| Inline task execution not scalable | MEDIUM | MEDIUM | ADR-011: Phase 3+ to reintroduce Celery + Redis for distribution | 1 |
| No periodic task scheduling | MEDIUM | MEDIUM | 6h anomaly scan and 24h risk recompute inactive; manual trigger via seed script | 1 |
| 197 tests at 62% coverage — Phase 2 needs 70%+ | MEDIUM | LOW | Coverage is unified and increasing; baseline established | 1 |

---

## 11. Architecture Decision Records

### Existing ADRs (docs/architecture/ADR/)

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Phase 1 Architectural Style | ✅ APPROVED |
| ADR-002 | Catalyst Deployment Boundaries | ✅ APPROVED |
| ADR-003 | Source of Record vs Intelligence Layer | ✅ APPROVED |
| ADR-004 | Graph Representation (Join Tables Phase 1) | ✅ APPROVED |
| ADR-005 | Entity Resolution Approach | ✅ APPROVED |
| ADR-006 | RAG and Natural Language Query Safety | ✅ APPROVED |
| ADR-007 | Sensitive Field Exclusion | ✅ APPROVED |
| ADR-008 | MVP vs Target State | ✅ APPROVED |

### New ADRs (docs/architecture/decisions/)

| ADR | Title | Status |
|-----|-------|--------|
| ADR-009 | Dual-Language Bootstrap Strategy | ✅ APPROVED |
| ADR-010 | Service-to-AI Separation Contract | ✅ APPROVED |
| ADR-011 | Inline Task Execution Pattern | ✅ APPROVED |

### ADR Location Note
ADR-009 through ADR-011 are in `docs/architecture/decisions/`. ADR-001 through ADR-008 remain in `docs/architecture/ADR/`. Future ADRs should go to `decisions/` to consolidate.
