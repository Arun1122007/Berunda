# Phase 1 — Validated Architecture

**Document ID:** BERUNDA-ARCH-VAL-001 | **Version:** 1.0 | **Status:** APPROVED
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-20

---

## 1. Architecture Summary

Berunda uses a **Modular Functions + API Gateway** architecture deployed on Zoho Catalyst.

### Architectural Style

- **Phase 1:** Modular Catalyst Functions with synchronous REST calls, API Gateway routing, Catalyst Data Store persistence
- **Target (Phase 3+):** Event-driven mesh with Catalyst Signals event bus, Circuits workflow orchestration, CQRS

### Key Principle

All services operate within a single Zoho Catalyst project. No external cloud infrastructure is required. This is mandated by the Hack2Skill Datathon 2026 rules.

---

## 2. System Components

| Component | Technology | Responsibility | Existing? |
|---|---|---|---|
| **Frontend SPA** | React 18 + TypeScript + Vite | User interface, data visualization | ✅ Scaffolded |
| **API Gateway** | Catalyst API Gateway | Auth, routing, rate limiting | ⬜ Catalyst-managed |
| **FIR Ingestion** | Catalyst Function (Node.js) | Parse, validate, import FIR data | ⬜ Placeholder |
| **NER Extraction** | Catalyst Function (Node.js/Python) | Entity extraction from FIR narratives | ⬜ Placeholder |
| **Entity Resolution** | Catalyst Function (Node.js) | Cross-case person matching | ⬜ Placeholder |
| **Risk Scoring** | Catalyst AppSail (Python) | Explainable repeat-offender scores | ⬜ Placeholder |
| **Hotspot Analysis** | Catalyst Function (Node.js) | KDE/hexbin hotspot detection | ⬜ Placeholder |
| **Anomaly Detection** | Catalyst Function (Node.js) | Z-score spike detection | ⬜ Placeholder |
| **Link Analysis** | Catalyst AppSail (Python/NetworkX) | Graph traversal over relationships | ⬜ Placeholder |
| **RAG Query** | Catalyst QuickML | NL Q&A over case corpus | ⬜ Placeholder |
| **Auth & RBAC** | Catalyst Auth | User auth + role-based access | ✅ Middleware scaffolded |
| **Audit Logging** | Catalyst Function (Node.js) | Immutable audit trail | ✅ Middleware scaffolded |
| **Fairness Check** | Catalyst Function (Node.js) | Model exclusion verification | ⬜ Placeholder |
| **Background Worker** | Node.js worker | Async processing | ⬜ Placeholder |

---

## 3. Component Responsibilities

### Frontend (`apps/web/`)
- React SPA with route-based code splitting
- MapLibre GL for geospatial hotspot visualization
- Cytoscape.js for relationship link graphs
- Recharts for analytics dashboards
- RAG chat interface for "Ask Berunda"
- All API calls through centralized `apiClient`
- Route protection via `ProtectedRoute` component
- 5 feature modules: Dashboard, Hotspot, Graph, Analytics, RAG, Admin

### API (`apps/api/`)
- Catalyst-deployed serverless functions (10 functions)
- Common middleware for auth, error handling, logging, audit, rate limiting, correlation
- Shared response/validation/error utilities
- Common configuration loader

### Python Source (`src/`)
- AI module: LLM integration, RAG pipeline, agent orchestration, prompt management
- ML module: risk scoring, feature engineering, model registry
- Pipelines: data ingestion, preprocessing, training, evaluation
- Shared: config, logging, validation utilities

### Worker (`apps/worker/`)
- Background job processing
- Catalyst-deployed worker function

---

## 4. Dependency Rules

### Layer Dependencies
```
apps/web  ──HTTP──>  apps/api (Catalyst Functions)
apps/api  ──calls──>  src/ai, src/ml (via Catalyst AppSail)
src/pipelines  ──>  src/shared
src/pipelines  ──>  src/ai
src/pipelines  ──>  src/ml
src/ai         ──>  src/shared
src/ml         ──>  src/shared
```

### Prohibited
- `src/shared` must NOT import from `src/ai`, `src/ml`, or `src/pipelines`
- No circular dependencies between Python modules
- No direct database access from frontend
- No secrets in source code
- No hardcoded environment-specific values

---

## 5. Data Flow Description

### FIR Ingestion Flow
```
User Upload → Frontend → API Gateway → FIR Ingestion Function
  → Validate Schema → Insert to DataStore
  → Trigger NER Extraction → Extract Entities → Write PersonEntityLink
  → Trigger Entity Resolution → Match Persons
  → Log Audit Event
```

### Query Flow
```
User Request → Frontend → API Gateway → Auth Check → Route to Function
  → Read from DataStore → Transform → Return Response
```

### RAG Query Flow
```
User Question → Frontend → API Gateway → RAG Function
  → Embed Query → Retrieve from Vector Store
  → Build Prompt → LLM Generate → Return Cited Answer
  → Log Audit Event
```

---

## 6. Trust Boundaries

| Boundary | Type | Description |
|---|---|---|
| Browser ↔ API Gateway | Network (HTTPS) | All external traffic must go through API Gateway |
| API Gateway ↔ Catalyst Functions | Internal Catalyst | Functions are not directly accessible externally |
| Functions ↔ Data Store | Internal Catalyst | Data access through Catalyst SDK only |
| AppSail ↔ ML Models | Internal Catalyst | Model inference within Catalyst network |

### Authentication Boundary
- Every request must pass through Catalyst API Gateway
- `auth.ts` middleware validates JWT tokens
- `requireRole()` enforces role-based access
- Frontend `ProtectedRoute` gates UI routes

### Authorization Boundary
- Admin: full access including system configuration
- Analyst: CRUD on case data, graph access, RAG queries
- Viewer: read-only access to dashboards and reports

---

## 7. Integration Boundaries

### External Integrations (Future)
- CCTNS: System of Record integration (Future-Restricted, legal MOU required)
- OpenStreetMap: Geospatial data for hotspot analysis
- Open-Meteo: Weather data for crime pattern analysis
- Bhuvan: Indian geospatial data (licensing unclear)

### Integration Pattern
- External APIs accessed through adapter layer in `src/shared/`
- All external calls wrapped with timeout, retry, circuit breaker
- Mock implementations for development and testing

---

## 8. Scaling Considerations

| Component | Scaling Strategy | Phase |
|---|---|---|
| Catalyst Functions | Auto-scaling per Catalyst | 1 |
| Data Store | Catalyst-managed with indexes | 1 |
| Frontend | Static file serving with CDN | 1 |
| RAG pipeline | Increase embedding cache, batch processing | 2 |
| Graph engine | Move from in-memory (NetworkX) to graph DB | 3 |

### Phase 1 Bottleneck
- Synchronous REST calls between functions
- In-memory graph processing with NetworkX (limited to demo dataset scale)
- Single-region deployment

---

## 9. Failure-Handling Approach

| Failure Mode | Handling Strategy |
|---|---|
| Function timeout | Catalyst function timeout (configured per function) |
| Data Store unavailable | Retry with exponential backoff (3 attempts) |
| External API failure | Circuit breaker with fallback to cached data |
| Invalid input | Schema validation at function boundary; return 400 |
| Authentication failure | Return 401; no stack trace in response |
| Unhandled exception | Global error handler returns safe 500 response |
| Rate limit exceeded | Return 429 with Retry-After header |

### Graceful Degradation
- Hotspot map falls back to cached data
- RAG offline → suggest pre-built reports
- Graph unavailable → show tabular data

---

## 10. Architectural Risks

| Risk | Impact | Likelihood | Mitigation | Phase |
|---|---|---|---|---|
| Catalyst API Gateway rate limits | Application unresponsive under load | Low | Configure rate limiting within limits; local dev bypass | 1 |
| Synchronous calls create cascading failures | Feature failures cascade | Medium | Add timeout + fallback per call | 2 |
| No dedicated graph DB | Performance at scale | Medium | Documented target for Phase 3+ | 1 |
| Catalyst vendor lock-in | Migration difficulty | Low | ADR-002 explicitly accepts this constraint | 1 |
| Missing nginx-spa.conf | Docker build failure | HIGH | Create immediately | 1 |

---

## 11. Architecture Decision Records

Existing ADRs (under `docs/architecture/ADR/`):

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Modular Functions + API Gateway (not microservices) | ✅ APPROVED |
| ADR-002 | All services within Catalyst project | ✅ APPROVED |
| ADR-003 | Separate source vs intelligence schemas | ✅ APPROVED |
| ADR-004 | Relational join tables for graph (Phase 1) | ✅ APPROVED |
| ADR-005 | Rule-based blocking + weighted similarity for ER | ✅ APPROVED |
| ADR-006 | Retrieval-before-generation for RAG safety | ✅ APPROVED |
| ADR-007 | Hard exclude Caste/Religion from models | ✅ APPROVED |
| ADR-008 | BUILDABLE scope only for MVP | ✅ APPROVED |

New ADRs created during Phase 1 validation:

| ADR | Decision | Status |
|---|---|---|
| ADR-009 | Dual-language bootstrap (Python + Node.js) | ✅ APPROVED |

See `docs/architecture/decisions/ADR-009-dual-language-bootstrap.md`
