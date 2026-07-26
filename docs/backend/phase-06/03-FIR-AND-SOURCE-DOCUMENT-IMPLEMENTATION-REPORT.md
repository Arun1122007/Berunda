# Phase 6 — FIR and Source Document Implementation Report

## 1. FIR Lifecycle

The FIR lifecycle is managed by a formal state machine in `src/domain/fir_lifecycle.py`:

**10 States:**
| ID | Status | Description |
|----|--------|-------------|
| 1 | Draft | Initial state, editable |
| 2 | Submitted | Awaiting registration |
| 3 | Registered | Officially registered |
| 4 | Assigned | Officer assigned |
| 5 | Under Investigation | Active investigation |
| 6 | Review Pending | Awaiting supervisor review |
| 7 | Resolved | Investigation complete |
| 8 | Closed | Case closed |
| 9 | Reopened | Reopened for further investigation |
| 10 | Archived | Final state, no further transitions |

**Transition Enforcement:**
- Invalid transitions return 404 with error message
- Terminal state (archived) has no outgoing transitions
- Assignment-required states add warnings
- Supervisor review states add warnings

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/fir/statuses/lifecycle` | List all states and transitions |
| GET | `/api/v1/fir/statuses/transitions` | Get allowed transitions for a status |

## 2. Source Document Preservation

The source document module (`src/domain/source_document.py`) ensures original FIR source is never overwritten:

**Source Types:** manual_text, uploaded_pdf, uploaded_doc, synthetic, imported

**Processing Status:** pending, processing, completed, failed

**Rules:**
- Original source text/PDF is stored separately from AI-processed data
- Source download requires authorization
- User-supplied filenames are validated for path traversal
- Synthetic data is explicitly marked
- Source version tracking for reprocessing history

## 3. FIR CRUD Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/fir` | JWT | List FIRs (district-scoped) |
| GET | `/api/v1/fir/{id}` | JWT | Get FIR detail with persons |
| POST | `/api/v1/fir` | admin/officer | Create FIR draft |
| PUT | `/api/v1/fir/{id}` | admin/officer | Update FIR |
| DELETE | `/api/v1/fir/{id}` | admin | Soft-delete FIR |
| PUT | `/api/v1/fir/{id}/status` | admin/officer/supervisor | Update status (validated) |

## 4. New Person Endpoints (Phase 6)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/fir/{id}/complainants` | List complainants for FIR |
| GET | `/api/v1/fir/{id}/victims` | List victims for FIR |
| GET | `/api/v1/fir/{id}/accused` | List accused for FIR |
| GET | `/api/v1/fir/{id}/act-sections` | List act/sections for FIR |

## 5. Police Stations (Phase 6)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/police-stations` | List all police stations |
| GET | `/api/v1/police-stations/{id}` | Get station details |
| GET | `/api/v1/police-stations/districts` | List all districts |
