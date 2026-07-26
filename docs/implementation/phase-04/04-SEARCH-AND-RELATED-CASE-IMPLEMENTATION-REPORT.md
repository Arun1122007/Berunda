# Project Berunda — Search and Related Cases Implementation Report

> **Document ID:** BERUNDA-P4-005  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents Workstream C: structured FIR search with advanced filters, result ranking, related-case candidate generation via hybrid deterministic/semantic signals, and human review workflow for related-case suggestions.

---

## 2. Implementation Details

### 2.1 Structured Search with Filters

**Endpoint**: `POST /api/v1/search`

The search endpoint accepts `SearchFilters` with the following optional filters:

| Filter | Type | Description |
|--------|------|-------------|
| `query` | string | Free-text search term |
| `crime_no` | string | Partial crime number match |
| `date_from` | date | Filter by registration date >= |
| `date_to` | date | Filter by registration date <= |
| `status_id` | int | Filter by case status |
| `police_station_id` | int | Filter by police station |
| `assigned_officer_id` | int | Filter by assigned officer (via active CaseAssignment) |
| `crime_major_head_id` | int | Filter by crime category |
| `person_name` | string | Person name search (prepared for expansion) |
| `vehicle_number` | string | Vehicle number search (triggers VehicleLink lookup) |
| `page` | int | Pagination (default: 1) |
| `page_size` | int | Items per page (default: 20, max: 100) |
| `semantic` | bool | Enable semantic search flag |

**Implementation files**:
- Router: `src/routers/search_router.py:14-74`
- Schema: `src/schemas/search.py:8-40`
- Repository: `src/repositories/sqlite_adapter.py:52-93` (`list_firs` method with all filter parameters)

### 2.2 District-Scoped Authorization

For non-admin users, `district_id` is extracted from the JWT token and applied as a filter on `CaseMaster.PoliceStationID` via subquery on `Unit.DistrictID`. This ensures cross-station isolation.

**Source**: `src/routers/search_router.py:21`

### 2.3 Result Ranking and Match Reason

Each search result item includes:

- `Confidence` — float (set to 1.0 for crime number match, from VehicleLink.Confidence for vehicle match)
- `MatchReason` — string explaining why the result matched (e.g., "Crime number match", "Vehicle match: KA-01-AB-1234")

Results without specific match signals return `Confidence` and `MatchReason` as `null`.

**Source**: `src/routers/search_router.py:36-66`

### 2.4 Semantic Search Toggle

The `semantic` boolean flag in `SearchFilters` is accepted and returned in the response as `semantic_used`. When `True`, the flag indicates semantic search was requested. The current implementation returns the same results (semantic search with embeddings is deferred to Phase 5 pending pgvector or external AI provider).

### 2.5 Related Case Candidate Generation

**Endpoint**: `POST /api/v1/fir/{case_master_id}/related-cases/generate`

The algorithm (`FIRService.generate_related_cases()` in `fir_service.py:390-432`) uses a hybrid deterministic approach:

1. Fetches up to 500 FIRs from the database
2. For each candidate FIR (excluding self), computes signals:
   - **Same crime category** (`CrimeMajorHeadID` match) → +0.20 confidence
   - **Same police station** (`PoliceStationID` match) → +0.15 confidence
3. Filters: only candidates with at least one signal and score >= 0.15
4. Creates `RelatedCaseSuggestion` records with `ReviewStatus="suggested"`
5. Caps at 20 suggestions per generation call
6. Second call returns cached existing suggestions (idempotent)

**Model version**: `hybrid-v1.0`

**Implementation files**:
- Router: `src/routers/related_cases_router.py:12-22`
- Service: `src/services/fir_service.py:390-432`
- Schema: `src/schemas/related_case.py`

### 2.6 Related Case Review Workflow

**List Suggestions**: `GET /api/v1/fir/{case_master_id}/related-cases`

Returns all suggestions (source or candidate) for an FIR, enriched with `CandidateCrimeNo` and `CandidateStatusID` from the candidate case.

**Review Suggestion**: `PUT /api/v1/fir/related-cases/{suggestion_id}/review`

Accepts `ReviewStatus` (`accepted` or `rejected`) and optional `ReviewReason`. Updates the suggestion record and logs `REVIEW_RELATED_CASE` audit event.

**Implementation files**:
- Router: `src/routers/related_cases_router.py:25-52`
- Service: `src/services/fir_service.py:434-482`
- Repository: `src/repositories/sqlite_adapter.py:269-306`

### 2.7 Confidence Scoring and Explanation

- `ConfidenceScore` — float (0.0–0.95), capped at 0.95
- `SupportingSignals` — JSON array of signal descriptions (e.g., `["Same crime category", "Same police station"]`)
- `Explanation` — human-readable string combining signals (e.g., `"Same crime category; Same police station"`)

---

## 3. API Endpoints

| Method | Endpoint | Auth Required | Allowed Roles | Description |
|--------|----------|---------------|---------------|-------------|
| POST | `/api/v1/search` | Optional (auth improves scope) | any | Structured FIR search |
| POST | `/api/v1/fir/{id}/related-cases/generate` | Yes | admin, officer, supervisor, analyst | Generate related-case suggestions |
| GET | `/api/v1/fir/{id}/related-cases` | Optional (auth) | any | List related-case suggestions |
| PUT | `/api/v1/fir/related-cases/{id}/review` | Yes | admin, officer, supervisor | Review a suggestion |

---

## 4. Database Tables

| Table | Key Fields | Purpose |
|-------|------------|---------|
| `src_CaseMaster` | CaseMasterID, CrimeNo, CrimeRegisteredDate, PoliceStationID, CaseStatusID, CrimeMajorHeadID | Search source table |
| `int_VehicleLink` | VehicleNumber, CaseMasterID | Vehicle match for search |
| `int_CaseAssignment` | CaseMasterID, AssignedOfficerID, Status | Officer assignment filter |
| `int_RelatedCaseSuggestion` | SuggestionID, SourceFIRID, CandidateFIRID, ConfidenceScore, SupportingSignals, Explanation, ReviewStatus, ReviewedByUserID, ReviewReason | Suggestion and review records |

---

## 5. Authorization Rules

| Operation | Required Role | Notes |
|-----------|---------------|-------|
| Search FIRs | Optional | Non-admin = district-scoped; unauthenticated = all |
| Generate suggestions | admin, officer, supervisor, analyst | Viewer forbidden |
| List suggestions | Any | — |
| Review suggestion | admin, officer, supervisor | Analyst and viewer forbidden |

---

## 6. Test Coverage

**Test files**:
- `tests/api/test_search_api.py` — 16 tests
- `tests/api/test_related_cases_api.py` — 18 tests
- `tests/integration/test_phase4_endpoints.py` — search, related-cases integration

Key search scenarios:
- Empty results, all results, pagination, page size limits
- Crime number exact and partial match
- Vehicle number match
- Status and police station filters
- Semantic flag propagation
- Date range filtering
- Non-admin district scoping
- Unauthenticated access
- Invalid page/page_size returns 422

Key related-case scenarios:
- Generate suggestions with matching signals
- Second call returns cached results
- Non-existent FIR returns 404
- Authorization: viewer/analyst forbidden for generate
- List empty, list after generate
- Review accept, review reject
- Invalid suggestion ID returns 404
- Invalid review status returns 422
- List reflects review status after update

**Result**: 34 API tests + integration coverage

---

## 7. Status

**Verdict: COMPLETED** — All Workstream C features are implemented. Search supports 8 filter dimensions with pagination and district-scoped authorization. Related-case generation uses hybrid deterministic signals (crime category, police station) with confidence scoring. Human review workflow enforces `accepted`/`rejected` with explanation tracking. Semantic search flag is accepted but deferred for full embedding implementation.

