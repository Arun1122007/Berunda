# 03 — Frontend and Backend Module Design

**Document ID:** BERUNDA-ARCH2-MODDES-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 module design baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document defines module boundaries so that both team members can work simultaneously without conflicts.
> No module may be added without a corresponding P0 or P1 feature requirement.
> Frontend and backend module boundaries enable one developer to work on each side independently.

---

## 1. Architecture Overview

```
Frontend (React SPA)                Backend (FastAPI on AppSail)
────────────────────                ─────────────────────────────
apps/web/src/                       src/
├── app/                            ├── main.py           (entry point)
│   ├── Router.tsx                  ├── middleware/
│   └── ProtectedRoute.tsx          │   ├── auth.py       (JWT + RBAC)
├── features/                       │   └── correlation.py
│   ├── auth/                       ├── routers/          (HTTP layer)
│   ├── dashboard/                  ├── services/         (business logic)
│   ├── cases/                      ├── pipelines/        (NER + resolution)
│   ├── ingestion/                  ├── ml/               (entity resolution)
│   ├── entities/                   ├── ai/               (providers + guardrails)
│   ├── graph/                      ├── models/           (ORM)
│   ├── hotspot/                    ├── schemas/          (Pydantic)
│   ├── anomalies/                  ├── repositories/     (data access)
│   ├── rag/                        ├── tasks/            (background)
│   ├── risk/                       └── shared/           (logging, config)
│   ├── audit/
│   ├── admin/
│   ├── analytics/
│   └── shared/
├── components/                 API Contract (OpenAPI 3.1)
├── hooks/                      ─────────────────────────
├── services/                   apps/web/src/services/api.ts  (typed client)
├── lib/
└── types/
```

---

## 2. Frontend Module Map

Only modules with MVP requirements are approved. `socioeconomic` is removed from navigation.

### APPROVED Frontend Modules

| Module | Folder | P Level | Roles That See It |
|--------|--------|---------|------------------|
| auth | `features/auth/` | P0 | All |
| dashboard | `features/dashboard/` | P0 | All (role-specific view) |
| cases | `features/cases/` | P0 | INVESTIGATOR, ADMIN |
| ingestion | `features/ingestion/` | P0 | INVESTIGATOR, ADMIN |
| entities | `features/entities/` | P0 | INVESTIGATOR, SCRB_ANALYST, ADMIN |
| graph | `features/graph/` | P0 | INVESTIGATOR, SCRB_ANALYST |
| hotspot | `features/hotspot/` | P0 | INVESTIGATOR, SCRB_ANALYST, ADMIN |
| anomalies | `features/anomalies/` | P0 | INVESTIGATOR, SCRB_ANALYST, ADMIN |
| rag | `features/rag/` | P0 | INVESTIGATOR, SCRB_ANALYST |
| risk | `features/risk/` | P0 | INVESTIGATOR, SCRB_ANALYST |
| audit | `features/audit/` | P0 | COMPLIANCE, ADMIN (full); INVESTIGATOR, SCRB_ANALYST (own-only) |
| admin | `features/admin/` | P0 | ADMIN |
| analytics | `features/analytics/` | P1 | SCRB_ANALYST, ADMIN |
| reports | `features/reports/` | P2 STRETCH | SCRB_ANALYST, COMPLIANCE |
| shared | `features/shared/` | P0 | All |

### REJECTED Frontend Module

| Module | Reason |
|--------|--------|
| `features/socioeconomic/` | Not in MVP scope; no Phase 1 requirement; remove from nav |

---

## 3. Frontend Routes and Screen Ownership

### Route Definitions

| Route | Module | Screen | Roles | Priority | Auth Required |
|-------|--------|--------|-------|---------|--------------|
| `/login` | auth | LoginPage | Public | P0 | No |
| `/` | dashboard | DashboardPage | All | P0 | Yes |
| `/cases` | cases | CaseListPage | INVESTIGATOR, ADMIN | P0 | Yes |
| `/cases/new` | cases | NewFIRForm | INVESTIGATOR, ADMIN | P0 | Yes |
| `/cases/:id` | cases | CaseDetailPage (tabs: Overview, Persons, Vehicles, Evidence, Timeline) | INVESTIGATOR, SCRB_ANALYST, ADMIN | P0 | Yes |
| `/cases/:id/upload` | ingestion | DocumentUploadPage | INVESTIGATOR, ADMIN | P0 | Yes |
| `/cases/:id/extraction` | entities | ExtractionReviewPage | INVESTIGATOR, ADMIN | P0 | Yes |
| `/entities` | entities | EntityListPage | INVESTIGATOR, SCRB_ANALYST, ADMIN | P0 | Yes |
| `/entities/:id` | entities | EntityProfilePage | INVESTIGATOR, SCRB_ANALYST, ADMIN | P0 | Yes |
| `/entities/merge-queue` | entities | MergeReviewQueuePage | INVESTIGATOR, ADMIN | P0 | Yes |
| `/entities/merge/:id` | entities | MergeDetailPage | INVESTIGATOR, ADMIN | P0 | Yes |
| `/graph/:entity_id` | graph | GraphCanvasPage | INVESTIGATOR, SCRB_ANALYST | P0 | Yes |
| `/search` | cases | GlobalSearchPage | All | P0 | Yes |
| `/hotspot` | hotspot | HotspotMapPage | INVESTIGATOR, SCRB_ANALYST, ADMIN | P0 | Yes |
| `/anomalies` | anomalies | AnomalyListPage | INVESTIGATOR, SCRB_ANALYST, ADMIN | P0 | Yes |
| `/rag` | rag | AskBerundaPage | INVESTIGATOR, SCRB_ANALYST | P0 | Yes |
| `/risk/:entity_id` | risk | RiskScorePage | INVESTIGATOR, SCRB_ANALYST | P0 | Yes |
| `/compliance/fairness` | entities | FairnessDashboardPage | COMPLIANCE, SCRB_ANALYST | P0 | Yes |
| `/audit` | audit | AuditLogPage | All (filtered by role) | P0 | Yes |
| `/admin/users` | admin | UserListPage | ADMIN | P0 | Yes |
| `/admin/users/new` | admin | CreateUserPage | ADMIN | P0 | Yes |
| `/analytics` | analytics | AnalyticsDashboardPage | SCRB_ANALYST, ADMIN | P1 | Yes |

---

## 4. Frontend Module Specifications

### Module: auth

| Field | Value |
|-------|-------|
| **Purpose** | Login, token storage, refresh, logout |
| **Routes** | `/login` |
| **Roles** | Public (unauthenticated) |
| **Screens** | LoginPage |
| **API deps** | `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout` |
| **Data displayed** | None (form only) |
| **Data edited** | Username, password (never persisted on frontend) |
| **State** | JWT access token in memory; role, district from decoded token |
| **Permission behavior** | Redirect to `/` on successful login; redirect to `/login` on 401 |
| **Error states** | "Invalid credentials"; "Account locked — contact admin"; network error |
| **Test** | Login success; invalid creds; account lockout |

---

### Module: cases

| Field | Value |
|-------|-------|
| **Purpose** | FIR list, FIR detail, manual FIR creation, status display |
| **Routes** | `/cases`, `/cases/new`, `/cases/:id`, `/search` |
| **Roles** | INVESTIGATOR and ADMIN for create; all roles for view (jurisdiction scoped) |
| **Screens** | CaseListPage, NewFIRForm, CaseDetailPage (5 tabs) |
| **API deps** | `GET /api/v1/fir`, `POST /api/v1/fir`, `GET /api/v1/fir/:id`, `GET /api/v1/search` |
| **Data displayed** | CrimeNo, date, district, station, crime head, status, BriefFacts (read-only), accused list (no CasteRef), victim list, vehicles |
| **Data edited** | FIR form fields (create only; edit is P1) |
| **Permission behavior** | If INVESTIGATOR: only own-district cases shown (backend enforces); create restricted to own stations |
| **Error states** | 422 field errors shown per field; 403 on station mismatch; empty state for no cases |
| **Test** | FIR create success; FIR create missing field; cross-station 403; case detail all tabs |
| **Shared deps** | `shared/SyntheticDataBanner`, `shared/StatusBadge`, `shared/Pagination` |

---

### Module: ingestion

| Field | Value |
|-------|-------|
| **Purpose** | FIR document upload; extraction progress display |
| **Routes** | `/cases/:id/upload` |
| **Roles** | INVESTIGATOR, ADMIN |
| **Screens** | DocumentUploadPage |
| **API deps** | `POST /api/v1/fir/:id/upload` (multipart) |
| **Data displayed** | Upload progress; extraction status; file name, size, hash |
| **Permission behavior** | 415 error shown if wrong file type; 413 if too large |
| **Error states** | Upload failure; MIME type rejection; extraction_status = FAILED → show "Manual entry required" |
| **Notes** | Frontend validates file size before upload to prevent large request; MIME validated by backend |

---

### Module: entities

| Field | Value |
|-------|-------|
| **Purpose** | PersonEntity profile; extraction review; merge review queue; fairness dashboard |
| **Routes** | `/entities`, `/entities/:id`, `/entities/merge-queue`, `/entities/merge/:id`, `/cases/:id/extraction`, `/compliance/fairness` |
| **Roles** | INVESTIGATOR and ADMIN for merge; all roles for view (jurisdiction scoped) |
| **Screens** | EntityListPage, EntityProfilePage, ExtractionReviewPage, MergeReviewQueuePage, MergeDetailPage, FairnessDashboardPage |
| **API deps** | `GET /api/v1/entities`, `GET /api/v1/entities/:id`, `GET/POST /api/v1/fir/:id/extraction`, `GET /api/v1/entities/merge-queue`, `POST /api/v1/entities/merge/:id/approve`, `/reject`, `/defer`, `GET /api/v1/fairness` |
| **Key UI** | ExtractionReviewPage: 3 cards (person, vehicle, location); confidence colour-coded; AI_SUGGESTION label; Approve/Edit/Reject per card. MergeDetailPage: side-by-side comparison; confidence score; signal labels; approve/reject/defer buttons |
| **Permission behavior** | Fairness dashboard: COMPLIANCE (full feature list), SCRB_ANALYST (read-only summary), INVESTIGATOR → 403 |
| **AI label** | "AI suggestion — review required" label must be visible on all extraction cards |

---

### Module: graph

| Field | Value |
|-------|-------|
| **Purpose** | Cytoscape.js relationship graph; BFS path query |
| **Routes** | `/graph/:entity_id` |
| **Roles** | INVESTIGATOR (own district scope), SCRB_ANALYST |
| **Screens** | GraphCanvasPage |
| **API deps** | `GET /api/v1/graph/:entity_id?depth=2`, `POST /api/v1/graph/shortest-path {source, target}` |
| **Key UI** | Cytoscape.js canvas; node colour by type (person=orange, case=blue, vehicle=grey, location=green); edge labels; "Find hidden link" button with node selector; path highlight on BFS result |
| **Error states** | "No path found within 5 hops" if BFS returns empty; empty graph shows "No connections found" |
| **Audit** | GRAPH.VIEW event on load; GRAPH.SHORTESTPATH.QUERY on BFS |

---

### Module: hotspot

| Field | Value |
|-------|-------|
| **Purpose** | MapLibre GL heatmap; district drill-down; anomaly badges |
| **Routes** | `/hotspot` |
| **Roles** | INVESTIGATOR (own district), SCRB_ANALYST, ADMIN |
| **Screens** | HotspotMapPage |
| **API deps** | `GET /api/v1/hotspot?crime_head=&date_range=`, `GET /api/v1/anomaly`, `GET /api/v1/hotspot/district/:id` |
| **Key UI** | Karnataka district polygons on MapLibre; heatmap density overlay; crime-type dropdown; date-range picker (7d/30d/90d/custom); click district → side panel with station breakdown and case list link |
| **INVESTIGATOR** | Map shows only own district polygon; other districts grayed |
| **Anomaly badge** | Rendered as Cytoscape/SVG overlay or Mapbox popup at district centroid; colour by severity |

---

### Module: rag

| Field | Value |
|-------|-------|
| **Purpose** | Natural-language question interface (Ask Berunda) |
| **Routes** | `/rag` |
| **Roles** | INVESTIGATOR (jurisdiction-scoped), SCRB_ANALYST |
| **Screens** | AskBerundaPage |
| **API deps** | `POST /api/v1/rag/query {question}` |
| **Key UI** | Chat interface; question input; answer display with disclaimer; citations section (list of CrimeNos); MockProvider banner when active |
| **Disclaimer** | "This is an AI-generated summary. Verify against case records before taking action." — always visible below answer |
| **Protected-char refusal** | Display the refusal message verbatim; do not show a spinner on subsequent questions |
| **Error states** | API timeout → activate MockProvider locally; show banner; rate-limit 429 → "Please wait 1 minute" |

---

### Module: risk

| Field | Value |
|-------|-------|
| **Purpose** | Risk score display with feature importance |
| **Routes** | `/risk/:entity_id` |
| **Roles** | INVESTIGATOR (own district), SCRB_ANALYST |
| **Screens** | RiskScorePage |
| **API deps** | `GET /api/v1/risk/:entity_id` |
| **Key UI** | Score value (0.0–1.0) with severity badge (LOW/MEDIUM/HIGH/CRITICAL); bar chart of top 5 features with human-readable labels; "Fairness verified ✓" badge if last check = PASS; "⚠ Fairness check failed" banner if FAIL |
| **Risk Score Not Available** | "Insufficient case history to compute a risk score" if < 2 prior cases |
| **AI label** | "Risk score is AI-generated — verify before taking investigative action." |

---

### Module: audit

| Field | Value |
|-------|-------|
| **Purpose** | Audit log view |
| **Routes** | `/audit` |
| **Roles** | All (filtered by role) |
| **API deps** | `GET /api/v1/audit?date_from=&user_id=&event_type=` |
| **Key UI** | Table: timestamp, event_type, user_id, resource_id, district; filter bar; no delete/edit controls |
| **INVESTIGATOR** | Sees only own entries (backend enforces — frontend cannot override) |
| **COMPLIANCE/ADMIN** | Sees all entries; user_id filter available |
| **Read-only** | No edit, no delete, no export in MVP |

---

### Module: admin

| Field | Value |
|-------|-------|
| **Purpose** | User lifecycle management |
| **Routes** | `/admin/users`, `/admin/users/new` |
| **Roles** | ADMIN only |
| **API deps** | `GET /api/v1/admin/users`, `POST /api/v1/admin/users`, `PATCH /api/v1/admin/users/:id/role`, `POST /api/v1/admin/users/:id/deactivate`, `POST /api/v1/admin/users/:id/unlock` |
| **Screens** | UserListPage (table with role, district, status), CreateUserPage (form) |

---

### Module: shared

| Component | Purpose | Used By |
|-----------|---------|---------|
| `SyntheticDataBanner` | "SYNTHETIC DATA" banner — must appear on every data-displaying page | All |
| `AILabel` | "AI suggestion — review required" label | entities, risk, rag |
| `StatusBadge` | Case status chip (REGISTERED, EXTRACTION_PENDING, etc.) | cases, dashboard |
| `ConfidenceChip` | Confidence % with colour coding (green/amber/red) | entities/ExtractionReview |
| `Pagination` | Standard paginated list | cases, entities, audit |
| `LoadingSpinner` | Async loading state | All |
| `ErrorBoundary` | React error boundary — prevents full-page crashes | All |
| `EmptyState` | Illustrated empty state for zero-result views | All |
| `MockProviderBanner` | "AI assistant is in limited mode" banner | rag, entities |
| `RoleBadge` | Displays the logged-in user's role | nav/header |

---

## 5. Frontend State Boundaries

| State Category | Store | Scope | Notes |
|---------------|-------|-------|-------|
| Auth token + user context | React Context (AuthContext) | App-wide | Access token in memory; NOT in localStorage |
| Role + district | AuthContext | App-wide | Decoded from JWT on login |
| FIR list / search results | TanStack Query (server state) | Feature | Cache 60s |
| Active FIR detail | TanStack Query | Feature | Invalidate on status change |
| Extraction queue | TanStack Query | Feature | Invalidate on approve |
| Merge queue | TanStack Query | Feature | Invalidate on merge decision |
| Graph data | TanStack Query | Feature | No cache (graph is built per request) |
| RAG conversation history | Local component state | Page | Cleared on page leave |
| Hotspot filter state | Local component state | Page | Crime type + date range |
| Cytoscape graph instance | Ref (useRef) | Page | Not in React state |

**Rule:** No sensitive data (BriefFacts, extracted entities, personal data) may be stored in localStorage or sessionStorage. Memory-only.

---

## 6. Frontend API Integration

All API calls go through a typed client at `apps/web/src/services/api.ts`:

```typescript
// Standard API call pattern
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
});

// Request interceptor: attach JWT from AuthContext
apiClient.interceptors.request.use(config => {
  const token = authContext.accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor: handle 401 → refresh token; handle 403 → show access-denied
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) { /* trigger refresh */ }
    if (error.response?.status === 403) { /* show AccessDeniedToast */ }
    return Promise.reject(error);
  }
);
```

**Correlation ID:** All requests include `X-Correlation-ID` header (generated client-side UUID).

**Shared contracts — TypeScript types:**
```typescript
// Shared error response type
interface ApiError {
  error: { code: string; message: string; detail?: Record<string, unknown> }
}

// Shared pagination
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
}

// Shared AI metadata
interface AIMetadata {
  is_ai_generated: boolean;
  confidence?: number;
  model_version?: string;
  provider?: 'openai' | 'groq' | 'mock';
}
```

---

## 7. Frontend Authorization Behavior

The frontend enforces **UX-level** access control only. Backend authorization is authoritative.

| Mechanism | Scope | Note |
|-----------|-------|------|
| `ProtectedRoute` wrapper | Route-level redirect for unauthenticated users | Does not replace backend auth |
| Role-based nav items | Hide nav items not relevant to role | Display only — backend still enforces |
| CasteRef/ReligionRef | Never rendered in any component — backend never sends them | Not a frontend decision |
| INVESTIGATOR district filter | Display note "Showing cases from [district]" | Backend enforces actual filter |
| ADMIN-only pages | Nav items and routes hidden for non-ADMIN | Backend returns 403 if accessed directly |

---

## 8. Backend Module Map

### L5 — Routers (HTTP interface)

| Router | File | Prefix | Methods | Roles |
|--------|------|--------|---------|-------|
| auth | `routers/auth_router.py` | `/api/v1/auth` | POST login/register/refresh/logout | Public (login); authenticated (others) |
| fir | `routers/fir_router.py` | `/api/v1/fir` | GET list, GET :id, POST create, POST :id/upload, GET :id/extraction, POST :id/extraction/approve | INVESTIGATOR, ADMIN (create/upload); all (view) |
| entity | `routers/entity_router.py` | `/api/v1/entities` | GET list, GET :id, GET merge-queue, POST merge/:id/approve|reject|defer | All (view); INVESTIGATOR/ADMIN (merge) |
| graph | `routers/graph_router.py` | `/api/v1/graph` | GET :entity_id, POST shortest-path | INVESTIGATOR, SCRB_ANALYST |
| hotspot | `routers/hotspot_router.py` | `/api/v1/hotspot` | GET, GET /district/:id | INVESTIGATOR, SCRB_ANALYST, ADMIN |
| anomaly | `routers/anomaly_router.py` | `/api/v1/anomaly` | GET list, GET :id | INVESTIGATOR, SCRB_ANALYST, ADMIN |
| risk | `routers/risk_router.py` | `/api/v1/risk` | GET :entity_id, POST /batch-compute | INVESTIGATOR, SCRB_ANALYST (view); ADMIN (batch) |
| rag | `routers/rag_router.py` | `/api/v1/rag` | POST /query (rate-limited 5/min) | INVESTIGATOR, SCRB_ANALYST |
| fairness | `routers/fairness_router.py` | `/api/v1/fairness` | GET /dashboard, POST /check | COMPLIANCE, SCRB_ANALYST (view); ADMIN (trigger) |
| audit | `routers/audit_router.py` | `/api/v1/audit` | GET (own-only for INVESTIGATOR/SCRB_ANALYST; all for COMPLIANCE/ADMIN) | All |
| admin | `routers/admin_router.py` *(new)* | `/api/v1/admin` | GET/POST /users, PATCH /users/:id/role, POST /users/:id/deactivate|unlock | ADMIN |
| search | *(add to fir_router)* | `/api/v1/search` | GET ?q=&types= | All |
| health | `main.py` | `/health`, `/ready` | GET | Public |

---

## 9. Backend Layering

```
L6: Entry — main.py, worker.py
     ↓ (imports)
L5: Routers — routers/*.py
     ↓ (dependency injection via FastAPI Depends)
L4: Services — services/*.py (business logic, orchestration)
     ↓
L3: AI/ML/Pipelines — ai/*.py, ml/*.py, pipelines/*.py
     ↓
L2: Schemas — schemas/*.py (Pydantic request/response)
     ↓
L1: Models — models/*.py (SQLAlchemy ORM)
     ↓
L0: Foundation — shared/*.py, database.py, middleware/*.py, config.py
```

### Dependency Rules

| From | To | Allowed? |
|------|-----|---------|
| L5 Routers | L4 Services | ✅ Yes — primary pattern |
| L5 Routers | L0 Foundation | ✅ Yes — for `get_db`, `get_current_user` |
| L5 Routers | L1 Models | ❌ No — never access DB from router |
| L4 Services | L3 AI/ML | ✅ Yes — via adapter; see ADR-010 |
| L4 Services | L1 Models | ✅ Yes — via async session |
| L4 Services | other L4 Services | ⚠ Allowed only via DI, not direct import cycles |
| L3 AI | L4 Services | ❌ No — would create circular dependency |
| L3 AI | L2 Schemas | ✅ Yes |
| L3 AI | L1 Models | ✅ Yes (read-only) |
| Any | L0 shared | ✅ Yes |
| L1 Models | L0 shared | ✅ Yes (Base class) |
| L1 Models | L2+ | ❌ No |

---

## 10. Domain Ownership

| Domain | Owns Tables | Owned By Router/Service | Other Modules May Read? |
|--------|-----------|------------------------|------------------------|
| Auth | `auth_User`, `auth_RefreshToken` | auth_router, auth_service | Only via `get_current_user()` |
| FIR | `src_CaseMaster`, `src_Inv_OccuranceTime`, `int_FIRProcessingState` | fir_router, fir_service | Read-only by entity, graph, rag services |
| Evidence | `src_EvidenceMaster` | fir_router, fir_service | Read-only by entity service |
| Entity | `int_PersonEntity`, `int_PersonEntityLink`, `int_AIExtractionQueue`, `int_ERMergeCandidate` | entity_router, entity_service | Read-only by graph, risk, rag services |
| Vehicle | `int_VehicleLink` | entity_router, entity_service | Read-only by graph service |
| Graph | `int_RelationshipEdge` | graph_router, graph_service, graph_analytics_service | Read-only by rag service |
| Hotspot | `int_HotspotLayer` | hotspot_router, hotspot_service | None |
| Anomaly | `int_AnomalyAlert` | anomaly_router, anomaly_service | None |
| Risk | `int_RiskScore`, `int_RiskScoreFeatureImportance` | risk_router, risk_service | Read-only by entity service (for profile) |
| RAG | `int_RAGCorpusChunk` | rag_router, rag_service | None |
| Fairness | `gov_FairnessCheckResult` | fairness_router, fairness_service | risk_service (reads PASS/FAIL) |
| Audit | `gov_AuditLog` | audit_router, audit_service | All services (write-only via audit_service) |
| Lookup | `src_District`, `src_Unit`, `src_CrimeHead`, etc. | Shared reads | All services (read-only) |

---

## 11. Transaction Boundaries

| Operation | Transaction Scope | Notes |
|-----------|-----------------|-------|
| FIR create | Single transaction: INSERT CaseMaster + INSERT Inv_OccuranceTime | NER trigger is BackgroundTask (outside transaction) |
| FIR upload | Single transaction: INSERT EvidenceMaster + INSERT FIRProcessingState | Stratus upload before DB insert; rollback if DB fails |
| Extraction approve | Single transaction: INSERT target table + UPDATE extraction queue | Audit event in same transaction |
| Merge approve | Single transaction: UPDATE PersonEntity + UPDATE PersonEntityLink + UPDATE ERMergeCandidate | All or nothing |
| Risk scoring batch | One transaction per PersonEntity | Partial failure is logged; other entities continue |
| Audit write | In same async session as triggering operation, before commit | If audit fails: log error, don't rollback main transaction |

---

## 12. Error-Handling Standards

### HTTP Error Responses

All errors use the shared error response schema:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "detail": { "field": "error description" }
  }
}
```

### Error Code Registry

| HTTP Status | Code | When |
|-------------|------|------|
| 400 | VALIDATION_ERROR | Pydantic schema failure |
| 401 | UNAUTHORIZED | Missing or invalid JWT |
| 401 | TOKEN_EXPIRED | JWT access token expired |
| 403 | ACCESS_DENIED | Insufficient role |
| 403 | JURISDICTION_DENIED | Cross-district access by INVESTIGATOR |
| 403 | ACCOUNT_LOCKED | Too many failed login attempts |
| 404 | NOT_FOUND | Resource does not exist |
| 409 | CONFLICT | Duplicate CrimeNo or username |
| 413 | FILE_TOO_LARGE | Upload exceeds size limit |
| 415 | UNSUPPORTED_MEDIA_TYPE | Invalid MIME type |
| 422 | UNPROCESSABLE_ENTITY | Business rule violation (e.g., future OccurrenceDate) |
| 429 | RATE_LIMITED | RAG endpoint rate limit exceeded |
| 503 | SERVICE_UNAVAILABLE | DB or Stratus unavailable |

### Backend Error Handling Chain

```
Exception raised in service
  → services/base.py BerundaError wrapper
  → main.py global_exception_handler
  → Standard error response body
  → Structured logger entry (never stack trace to client)
```

---

## 13. Configuration Standards

All configuration from environment variables via `src/config.py` (Pydantic Settings):

| Variable | Required | Default | Notes |
|----------|---------|---------|-------|
| `DATABASE_URL` | Yes | — | PostgreSQL DSN |
| `JWT_SECRET_KEY` | Yes | — | Min 256-bit hex string |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No | 15 | — |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | No | 7 | — |
| `OPENAI_API_KEY` | No | — | MockProvider used if absent |
| `GROQ_API_KEY` | No | — | Alternative LLM |
| `STRATUS_TOKEN` | No | — | Stratus upload/download |
| `STRATUS_BUCKET` | No | `berunda-fir-docs` | — |
| `CORS_ORIGINS` | No | `http://localhost:5173` | Comma-separated |
| `APP_ENV` | No | `development` | `development`, `production` |
| `LOG_LEVEL` | No | `INFO` | Structured log level |
| `SENTRY_DSN` | No | — | Error tracking |

No feature flags in MVP. No runtime config file (YAML config is advisory only per `shared/config.py`).

---

## 14. Logging Standards

All logging through `src/shared/logging.py` (`get_logger(__name__)`):

### Log Level Rules

| Level | When |
|-------|------|
| DEBUG | Internal state useful for debugging — not enabled in production |
| INFO | Normal operation events (startup, successful operations) |
| WARNING | Recoverable errors (audit write failure, AI fallback activated) |
| ERROR | Unrecoverable errors (DB unavailable, unhandled exception) |

### Mandatory Log Fields

Every log entry must include (added by CorrelationIDMiddleware):

```json
{
  "timestamp": "ISO 8601 UTC",
  "level": "INFO",
  "logger": "src.services.fir_service",
  "message": "FIR created",
  "correlation_id": "uuid4",
  "user_id": "123",
  "endpoint": "/api/v1/fir",
  "method": "POST",
  "status_code": 201,
  "duration_ms": 45
}
```

### Prohibited Log Fields

The following must never appear in any log entry: passwords, JWT token values, API keys, CasteRef/ReligionRef values, BriefFacts full text, full person names in connection with CrimeNo.

---

## 15. Proposed Folder Structures

### Backend (`src/`)

```
src/
├── main.py                      # FastAPI app entry; router registration
├── worker.py                    # Background task worker entry
├── config.py                    # Pydantic Settings; all env vars
├── database.py                  # SQLAlchemy async engine + session factory
├── dependencies.py              # get_db(), get_current_user() FastAPI deps
├── exceptions.py                # BerundaError hierarchy
│
├── middleware/
│   ├── auth.py                  # JWT decode, require_role(), get_current_user()
│   ├── correlation.py           # X-Correlation-ID injection
│   └── security_headers.py     # HSTS, CSP, X-Frame-Options
│
├── routers/
│   ├── __init__.py              # exports all routers
│   ├── auth_router.py
│   ├── fir_router.py            # + /search endpoint
│   ├── entity_router.py         # + /merge-queue, /merge/:id/approve|reject|defer
│   ├── graph_router.py
│   ├── hotspot_router.py
│   ├── anomaly_router.py
│   ├── risk_router.py
│   ├── rag_router.py
│   ├── fairness_router.py
│   ├── audit_router.py
│   ├── admin_router.py          # NEW — user management (ADMIN only)
│   └── notification_router.py
│
├── services/
│   ├── auth_service.py
│   ├── fir_service.py           # + generate_crime_no(), upload_document(), status_lifecycle()
│   ├── entity_service.py        # + get_extraction_queue(), process_review(), get_merge_queue()
│   ├── graph_service.py
│   ├── graph_analytics_service.py
│   ├── hotspot_service.py       # + get_district_breakdown()
│   ├── anomaly_service.py
│   ├── risk_service.py          # + check_fairness_before_batch()
│   ├── rag_service.py           # + district_scoped_chunk_retrieval()
│   ├── fairness_service.py      # + halt_signal_to_risk_service()
│   ├── audit_service.py
│   ├── embedding_service.py
│   ├── guardrails_service.py    # + protected_char_refusal_check()
│   ├── cache_service.py
│   ├── notification_service.py
│   └── admin_service.py         # NEW
│
├── pipelines/
│   ├── ner_pipeline.py          # spaCy NER → int_AIExtractionQueue
│   └── rag_corpus_builder.py   # BriefFacts → chunks → embeddings → int_RAGCorpusChunk
│
├── ml/
│   └── entity_resolution.py    # NEW — Soundex blocking + weighted scorer per ADR-005
│
├── ai/
│   ├── providers/
│   │   ├── base.py              # Abstract LLM provider interface
│   │   ├── openai_provider.py
│   │   ├── groq_provider.py
│   │   └── mock_provider.py     # Pre-scripted responses for 3 rehearsed questions
│   └── guardrails.py
│
├── models/
│   ├── base.py                  # SQLAlchemy Base
│   ├── auth_models.py           # auth_User (4-role enum), auth_RefreshToken
│   ├── src_models.py            # src_ tables — police records (+ add CasteRef/ReligionRef to Accused/Victim)
│   ├── int_models.py            # int_ tables (+ add AIExtractionQueue, ERMergeCandidate, FIRProcessingState)
│   ├── gov_models.py            # gov_AuditLog, gov_FairnessCheckResult
│   └── ai_models.py             # AI session metadata
│
├── schemas/
│   ├── auth_schemas.py
│   ├── fir_schemas.py           # Strict whitelist schemas — no ORM inheritance
│   ├── entity_schemas.py
│   ├── extraction_schemas.py    # NEW — ExtractionQueueItem, ExtractionDecision
│   ├── merge_schemas.py         # NEW — MergeCandidate, MergeDecision
│   ├── graph_schemas.py
│   ├── hotspot_schemas.py
│   ├── anomaly_schemas.py
│   ├── risk_schemas.py
│   ├── rag_schemas.py
│   ├── audit_schemas.py
│   ├── fairness_schemas.py
│   └── admin_schemas.py         # NEW
│
├── repositories/
│   └── (data access abstraction — optional for MVP; services may query directly)
│
├── tasks/
│   ├── ner_tasks.py             # BackgroundTasks wrapper for NER pipeline
│   ├── risk_tasks.py            # BackgroundTasks wrapper for risk batch
│   ├── anomaly_tasks.py         # BackgroundTasks wrapper for anomaly detection
│   └── rag_corpus_tasks.py      # BackgroundTasks wrapper for corpus rebuild
│
├── alembic/
│   └── versions/                # Migrations — add 3 new migration files
│
└── shared/
    ├── logging.py               # Structured JSON logger
    ├── config.py                # YAML config loader (advisory)
    └── constants.py             # Enums: Role, FIRStatus, ExtractionStatus, AlertLevel
```

### Frontend (`apps/web/`)

```
apps/web/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── package.json
│
└── src/
    ├── main.tsx                 # React mount; providers
    ├── vite-env.d.ts
    │
    ├── app/
    │   ├── Router.tsx           # Route definitions; all routes
    │   └── ProtectedRoute.tsx   # Role + auth guard
    │
    ├── features/
    │   ├── auth/
    │   │   ├── LoginPage.tsx
    │   │   └── AuthContext.tsx  # JWT storage, role, district, refresh
    │   ├── dashboard/
    │   │   └── DashboardPage.tsx  # Role-specific landing
    │   ├── cases/
    │   │   ├── CaseListPage.tsx
    │   │   ├── CaseDetailPage.tsx  # Tabs: Overview, Persons, Vehicles, Evidence, Timeline
    │   │   ├── NewFIRForm.tsx
    │   │   └── GlobalSearchPage.tsx
    │   ├── ingestion/
    │   │   └── DocumentUploadPage.tsx
    │   ├── entities/
    │   │   ├── EntityListPage.tsx
    │   │   ├── EntityProfilePage.tsx
    │   │   ├── ExtractionReviewPage.tsx  # AI extraction review cards
    │   │   ├── MergeReviewQueuePage.tsx
    │   │   ├── MergeDetailPage.tsx       # Side-by-side comparison
    │   │   └── FairnessDashboardPage.tsx
    │   ├── graph/
    │   │   └── GraphCanvasPage.tsx  # Cytoscape.js + BFS panel
    │   ├── hotspot/
    │   │   └── HotspotMapPage.tsx   # MapLibre GL + district panel
    │   ├── anomalies/
    │   │   └── AnomalyListPage.tsx
    │   ├── rag/
    │   │   └── AskBerundaPage.tsx   # Chat interface + citations
    │   ├── risk/
    │   │   └── RiskScorePage.tsx    # Score + feature importance bar chart
    │   ├── audit/
    │   │   └── AuditLogPage.tsx
    │   ├── admin/
    │   │   ├── UserListPage.tsx
    │   │   └── CreateUserPage.tsx
    │   ├── analytics/              # P1 — temporal charts
    │   │   └── AnalyticsDashboardPage.tsx
    │   └── shared/
    │       ├── SyntheticDataBanner.tsx
    │       ├── AILabel.tsx
    │       ├── StatusBadge.tsx
    │       ├── ConfidenceChip.tsx
    │       ├── Pagination.tsx
    │       ├── LoadingSpinner.tsx
    │       ├── ErrorBoundary.tsx
    │       ├── EmptyState.tsx
    │       ├── MockProviderBanner.tsx
    │       └── RoleBadge.tsx
    │
    ├── components/              # Reusable cross-feature UI components
    │   └── layout/
    │       ├── AppShell.tsx     # Nav, sidebar, header
    │       └── Navbar.tsx       # Role-filtered nav items
    │
    ├── hooks/
    │   ├── useAuth.ts           # Access AuthContext
    │   ├── useCurrentUser.ts    # Decode and expose role/district
    │   └── useApiQuery.ts       # TanStack Query wrapper with error handling
    │
    ├── services/
    │   └── api.ts               # Typed axios client; interceptors; JWT handling
    │
    ├── lib/
    │   └── queryClient.ts       # TanStack Query configuration
    │
    └── types/
        ├── api.d.ts             # Shared API types (ApiError, PaginatedResponse, AIMetadata)
        ├── fir.d.ts
        ├── entity.d.ts
        ├── graph.d.ts
        └── auth.d.ts
```

---

## 16. Parallel-Development Boundaries

The two-person team can work in parallel using API contracts as the synchronisation point:

| Developer A (Backend) | Developer B (Frontend) |
|-----------------------|----------------------|
| Implement FIR router, service, CrimeNo generation | Use mock API responses for FIR list and create screens |
| Implement entity resolution algorithm | Build ExtractionReviewPage using mock extraction queue data |
| Implement merge review endpoints | Build MergeDetailPage using mock merge candidate data |
| Implement RAG jurisdiction scoping | Build AskBerundaPage with mock RAG responses |
| Implement risk scoring + feature importance | Build RiskScorePage with mock score data |
| Deploy Catalyst schema + seed data | Implement hotspot map and anomaly badges (static data works) |

**Contract freeze required:** API request and response schemas for FIR create, extraction review, merge decision, RAG query, and risk score must be agreed and documented in `schemas/*.py` before parallel work begins. Frontend uses these schemas as TypeScript types.

---

## 17. Module Test Responsibilities

| Module | Unit Tests | Integration Tests | Test Data |
|--------|-----------|-----------------|---------|
| auth | `test_auth_service.py` — login, lockout, refresh | `test_auth_router.py` — HTTP flows | Fixture users |
| fir | `test_fir_service.py` — CrimeNo gen, status machine | `test_fir_router.py` — create, upload, jurisdiction | Synthetic FIRs |
| entity | `test_entity_service.py` — extraction review, merge | `test_entity_router.py` — queue, approve, reject | Planted repeat offender |
| entity_resolution | `test_ml_entity_resolution.py` — Soundex, scoring | Integration with entity_service | Planted name variants |
| graph | `test_graph_service.py` — NetworkX graph build | `test_graph_router.py` — BFS path | Planted hidden link |
| rag | `test_rag_service.py` — jurisdiction scoping, guardrails | `test_rag_router.py` — 3 rehearsed questions | Planted cases |
| risk | `test_risk_service.py` — feature list validation, score range | `test_risk_router.py` — view, batch | Planted high-risk person |
| fairness | `test_fairness_service.py` — PASS/FAIL, halt condition | `test_fairness_router.py` | None (test feature lists) |
| audit | `test_audit_service.py` — write, immutability | `test_audit_router.py` — own-only filter | Generated by other tests |
| seed | `test_seed_planted_patterns.py` | All planted pattern assertions (AC-SEED-001) | Seed dataset |

**Coverage target:** ≥ 70% for all P0 service code paths (NFR-ESM-001).

---

## 18. Deferred Modules

| Module | Phase | Reason |
|--------|-------|--------|
| `notifications` | P2 | Push notification infrastructure not required for demo |
| `reports` | P2 stretch | Statutory reports not in P0/P1 |
| `socioeconomic` | NEVER (MVP) | Not in any approved requirement |
| `cctns_bridge` | Phase 2+ | Legal MOU required |

---

## 19. Open Decisions

| Decision | Status |
|----------|--------|
| Admin router: separate `admin_router.py` or extend `auth_router.py` | Recommend separate — cleaner boundary |
| TanStack Query vs SWR for frontend server state | Recommend TanStack Query — already in most React 18 stacks |
| Cytoscape.js React wrapper vs raw cytoscape | `cytoscape-react-cytoscapejs` wrapper recommended |
| MapLibre GL React integration | `react-map-gl` v8 with MapLibre GL JS recommended |

---

*End of 03-FRONTEND-AND-BACKEND-MODULE-DESIGN.md*
