# 01 — Architecture Principles and Constraints

**Document ID:** BERUNDA-ARCH2-PRINC-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 binding architecture principles
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> Every Phase 2 design decision must be evaluated against the principles in this document.
> A decision that violates a principle requires explicit justification and team approval.
> Principles cannot be overridden by individual implementation choices.

---

## 1. Principles

### PRINCIPLE-001 — Modular Design Within a Monolith

**Statement:** The system shall be structured as a modular monolith — all backend logic runs in a single Python process with clearly bounded modules. Module boundaries are enforced through explicit import rules (see `phase-1-validated-architecture.md` §4), not through separate deployable services.

**Rationale:** ADR-001 prohibits microservices in Phase 1/MVP. A 2-person team cannot manage inter-service communication, independent deployments, and distributed tracing within 11 days. Module boundaries provide the separation of concerns of microservices without the operational overhead.

**Implication:** No new deployable Python process is introduced unless required by Catalyst service boundaries (e.g., AppSail for Python ML runtime).

**Violation example:** Creating a separate FastAPI process for the audit service.

---

### PRINCIPLE-002 — Clear Frontend/Backend Separation

**Statement:** The frontend (React SPA) must never contain business logic, authorization decisions, or data-access code. The frontend calls the backend API; it validates inputs for user experience only. Authorization is never enforced only in the frontend.

**Rationale:** Frontend code is user-controlled. Authorization in the frontend can be bypassed by any client.

**Implication:** Every authorization check that protects data must exist in the backend `require_role()` middleware or service-layer filters, independently of what the frontend shows or hides.

**Violation example:** Hiding the "Compliance Dashboard" in the nav for the INVESTIGATOR role and treating that as the authorization.

---

### PRINCIPLE-003 — Backend-Enforced Authorization

**Statement:** The backend shall enforce all authorization checks before any sensitive data is returned or any state mutation is performed. The checks must be applied in this order: (1) JWT validity and expiry; (2) role check; (3) jurisdiction scope (DistrictID filter); (4) field-level exclusion (CasteRef/ReligionRef). All four checks are independent; passing one does not bypass another.

**Rationale:** FR-AUTH-003, FR-AUTH-004, FR-AUTH-005; ADR-007. Multiple authorization layers prevent privilege escalation through partial bypass.

**Implication:** All backend endpoints that return case, person, or vehicle data must apply filters (3) and (4) regardless of what role check (2) passes.

---

### PRINCIPLE-004 — Human-Reviewed AI Output

**Statement:** No AI-generated output (NER extraction, entity resolution suggestion, risk score, RAG answer) shall become an official system record without an explicit officer approval action. AI outputs shall be stored in staging tables and presented to the officer for review. Approval writes to the authoritative table.

**Rationale:** ADR-006; NFR-AI-002; DEC-006. Police records are legal documents. AI errors becoming official records without human verification create legal liability and operational risk.

**Violation example:** Auto-saving NER-extracted persons to `src_Accused` without showing a review screen.

---

### PRINCIPLE-005 — Source-Grounded AI Responses

**Statement:** The RAG system shall only answer questions based on retrieved document chunks from the corpus. The LLM system prompt must instruct the model to refuse to answer if grounding context is insufficient. Every RAG answer must include at least one citation. The guardrails service must refuse to return answers that violate this rule, regardless of LLM output.

**Rationale:** ADR-006; FR-AI-013; NFR-AI-004. Hallucinated answers about suspects in a policing context could cause serious harm.

**Implication:** The `guardrails_service.py` is not optional. The citation field is mandatory in the response schema.

---

### PRINCIPLE-006 — Privacy by Design

**Statement:** The system shall minimise personal data in API responses by design — not as an afterthought. Response schemas shall include only fields required for the requested operation. CasteRef and ReligionRef shall be excluded at the ORM SELECT level, not at serialisation. Individual-level sensitive records shall never be returned to INVESTIGATOR or SCRB_ANALYST roles.

**Rationale:** ADR-007; FR-AUTH-005; NFR-PRV-001; NFR-PRV-002.

**Implementation rule:** ORM queries for Accused, Victim, and ComplainantDetails records must explicitly exclude CasteRef and ReligionRef columns in the `with_entities()` or column projection, not rely on Pydantic excluding them at serialisation time.

---

### PRINCIPLE-007 — Auditability First

**Statement:** Audit events shall be written before the API response is returned. Every action on sensitive data — read, write, state change, AI operation, and administrative action — generates an audit event in `gov_AuditLog`. Audit write failure shall not block the user operation but shall be logged to a local error log.

**Rationale:** FR-AUD-001; NFR-AUT-001; NFR-AUT-002. Auditability is non-negotiable for a policing context and for the compliance demo step.

**Implication:** Every router endpoint that handles sensitive data must call `audit_service.log_event()` explicitly. This is not optional and must not be left to framework middleware alone.

---

### PRINCIPLE-008 — Data Minimisation

**Statement:** The system shall not collect, store, or transmit personal data beyond what is required for the immediate operation. Response payloads shall not include unused fields. Request payloads shall not accept unused fields.

**Rationale:** NFR-PRV-002; privacy-by-design.

**Implementation rule:** Every Pydantic response schema is a strict whitelist. No response schema shall inherit directly from an ORM model without explicit field selection.

---

### PRINCIPLE-009 — Secure File Handling

**Statement:** Uploaded files shall be validated by MIME type inspection of file content (not filename or Content-Type header). Files shall be staged in a temporary processing state. Only after validation — MIME check, size check, SHA-256 hash computation — shall the file be committed to Stratus. The original file is preserved; AI-processed output is always separate.

**Rationale:** FR-FIR-003; NFR-SEC-004; ADR-003.

**Violation example:** Trusting the `Content-Type` header of an upload request for MIME validation.

---

### PRINCIPLE-010 — Idempotent Operations Where Required

**Statement:** The following operations must be idempotent: (a) synthetic seed data load — running the seed script twice must not double the record count; (b) RAG corpus build — re-indexing must produce the same corpus state; (c) CrimeNo generation — a failed FIR create that is retried must not generate a second CrimeNo if the first was committed.

**Rationale:** NFR-INT-001; demo reliability (NFR-DEP-003).

**Implementation rule:** Seed scripts use UPSERT semantics. CrimeNo generation uses a database-level sequence with transaction rollback on FIR create failure.

---

### PRINCIPLE-011 — Failure Isolation

**Statement:** A failure in one module shall not cascade to unrelated modules. Specifically: (a) AI service failure must not prevent FIR viewing; (b) graph computation failure must not prevent case search; (c) audit write failure must not prevent the triggering operation. Each background task runs independently; failure in one task does not cancel others.

**Rationale:** NFR-REL-001; FEAT-006.

**Implementation rule:** All background tasks wrapped in `try/except`; failures logged but not re-raised to the caller. AI service calls always have a MockProvider fallback path.

---

### PRINCIPLE-012 — Observability

**Statement:** The system shall expose structured JSON logs from all request processing. Every log entry shall include request ID (correlation ID), endpoint, HTTP method, status code, processing time (ms), and user ID. The `/health` endpoint shall reflect true connectivity state. No sensitive data (passwords, JWT tokens, API keys, case content) shall appear in logs.

**Rationale:** NFR-OBS-001; NFR-OBS-002.

**Implementation rule:** `CorrelationIDMiddleware` is active. `src/shared/logging.py` provides the structured logger. No `print()` statements for operational output.

---

### PRINCIPLE-013 — Demo Reliability

**Statement:** Every P0 feature must have a fallback that allows the demo to continue if that feature fails. Specifically: AI services have MockProvider; the hotspot map has a tabular fallback; the graph has a list view fallback; the demo must not require manual data patches on Day 10 or later.

**Rationale:** NFR-REL-001; NFR-REL-002; NFR-REL-003; NFR-REL-004; SRSK-007.

**Implication:** Every P0 feature must be tested end-to-end with the seed dataset before Day 10. The fallback path must also be tested.

---

### PRINCIPLE-014 — Catalyst-Compatible Deployment

**Statement:** All production deployment shall use only Zoho Catalyst services as mandated by ADR-002. No external cloud infrastructure is introduced. Python ML-heavy components deploy on AppSail. Lightweight CRUD functions may deploy as Catalyst Functions. The database is Catalyst Data Store. Files are in Catalyst Stratus.

**Rationale:** ADR-002; hackathon mandatory rule.

**Implication:** Any Python package added to the backend must be installable in the AppSail environment. Any package that requires native compilation must be verified against the AppSail runtime.

---

### PRINCIPLE-015 — Avoid Unnecessary Distributed-System Complexity

**Statement:** Synchronous REST calls between components are preferred over message queues, event buses, or distributed caching in the MVP. Background tasks use FastAPI `BackgroundTasks` (ADR-011). Redis Cache is used only if a specific caching need justifies it. No new inter-process communication mechanism is introduced without justification.

**Rationale:** ADR-011; ADR-001. Distributed system complexity creates operational overhead that a 2-person hackathon team cannot manage.

---

### PRINCIPLE-016 — Avoid Premature Microservices

**Statement:** A module is not extracted into a separate deployable service unless it has an independent scaling requirement, a different runtime language requirement, or an independently failing dependency. In the MVP, the only justified service boundary is AppSail (Python ML runtime) vs Catalyst Functions (Node.js CRUD).

**Rationale:** ADR-001; ADR-008.

---

## 2. Constraints

### C-001 — Hackathon Timeline

**Constraint:** All P0 features must be complete and demoable by Day 10. P1 features must be complete by Day 8. No new P0 feature may be added after this document is approved. No P2 feature work may begin before all P0 features are passing acceptance tests.

**Source:** 04-MVP-SCOPE-AND-PRIORITIZATION.md §15

---

### C-002 — Synthetic / Anonymised Data Only

**Constraint:** No real KSP or CCTNS data may be loaded into any environment — development, test, or demo. All data must be synthetically generated. Every data record must include a `data_source: SYNTHETIC` field or label.

**Source:** AGENTS.md Rule 4; NFR-DEP-002.

---

### C-003 — Team Size

**Constraint:** The implementation team is exactly 2 people. No task may be designed that requires 3 or more simultaneous parallel implementations. Architecture must support one person working on backend while the other works on frontend, without blocking dependencies.

**Source:** 00-PHASE-1-INPUT-AND-ARCHITECTURE-AUDIT.md §2.

**Implication:** API contracts (request and response schemas) must be defined and frozen before parallel development begins. Mock API responses must be available for frontend development before backend endpoints are complete.

---

### C-004 — Approved Technology Stack

**Constraint:** Only the technologies in the approved technology stack (see `phase-1-validated-architecture.md` §2) may be used without team review. New dependencies require justification and review against Catalyst compatibility.

**Current approved stack:**

| Layer | Technology |
|-------|-----------|
| Backend API | Python FastAPI ≥ 0.115.0 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | PyJWT + bcrypt |
| ML | scikit-learn, NetworkX, spaCy en_core_web_md |
| NLP provider | OpenAI / Groq / MockProvider |
| Embeddings | OpenAI text-embedding-3-small |
| Vector search | FAISS (in-process) |
| Frontend | React 18 + TypeScript + Vite |
| Map | MapLibre GL JS |
| Graph viz | Cytoscape.js |
| Charts | Recharts |
| Container | Docker Compose (local dev) |
| CI | GitHub Actions |
| Monitoring | Prometheus + Grafana (local) |

---

### C-005 — Catalyst Boundaries

**Constraint:** All production deployment must use Catalyst services only (ADR-002). No AWS, GCP, Azure, or external cloud services. No Neo4j Cloud (ADR-004). No external Elasticsearch or Pinecone (ADR-006 — use FAISS in-process).

---

### C-006 — AI Provider Availability

**Constraint:** The demo must function when the LLM API (OpenAI/Groq) is unavailable. The MockProvider must be available as a fallback for all AI operations at any time. MockProvider responses for the 3 rehearsed RAG questions must be pre-scripted.

**Source:** NFR-REL-001; FR-AI-012; SRSK-004.

---

### C-007 — File Storage Limitations

**Constraint:** Uploaded files must be ≤ 10 MB (PDF) or ≤ 5 MB (image). Catalyst Stratus storage limits are unverified against the hackathon project tier. MVP uploads only PDF files for text extraction. Image-based OCR is deferred.

**Source:** FR-FIR-003; ARCH-DEC-007.

---

### C-008 — Demo-Network Reliability

**Constraint:** The demo must not depend on a reliable external network connection during judging. All AI operations must have a MockProvider fallback that does not require any external API call. The MapLibre tile server must fall back to a locally cached tile set if the OSM tile server is unreachable.

**Source:** NFR-REL-001; SRSK-004.

---

### C-009 — External API Availability

**Constraint:** OpenAI, Groq, and OSM Overpass APIs are not guaranteed available during demo. All calls to these services must have: (a) a 30-second timeout; (b) a fallback return value; (c) an error logged to the structured logger. No external API call may block a user-visible operation for more than 5 seconds.

**Source:** NFR-REL-001; C-008.

---

## 3. Architecture Decision Register

| ARCH-DEC-ID | Decision Required | Context | Options | Recommendation | Impact | Status | Related FRs |
|-------------|-----------------|---------|---------|---------------|--------|--------|------------|
| ARCH-DEC-001 | Demo deployment: AppSail vs Functions | AppSail runs Python; Functions runs Node.js; ADR-009 permits dual | A: AppSail for all; B: Functions for CRUD, AppSail for ML; C: AppSail only | **B** — Hybrid: AppSail hosts FastAPI; Functions handle lightweight routes | High — deployment architecture | OPEN — ADR required | All P0 |
| ARCH-DEC-002 | AI extraction queue storage | Suggestions need persistence between NER run and officer review | A: DB table; B: Redis; C: in-memory | **A — DB table** `int_AIExtractionQueue` | Medium | DECIDED — implement | FR-AI-001, FR-AI-003 |
| ARCH-DEC-003 | Entity resolution merge queue | Candidates need persistence | A: DB table; B: Redis | **A — DB table** `int_ERMergeCandidate` | Medium | DECIDED — implement | FR-AI-005, FR-AI-006 |
| ARCH-DEC-004 | Role name migration (3→4) | Existing code uses admin/analyst/viewer | A: Rename in middleware enum; B: Map at auth boundary | **A — Rename** — enum values in `auth_models.py` | Low-Medium | DECIDED — implement | FR-AUTH-003 |
| ARCH-DEC-005 | File upload pipeline | Need MIME validation from content | A: Stream+validate; B: Buffer+hash+validate | **B — buffer+validate** | Low | DECIDED | FR-FIR-003 |
| ARCH-DEC-006 | RAG vector indexing | Where do embedding vectors live? | A: FAISS in-process; B: pgvector; C: Catalyst NoSQL | **A — FAISS in-process** for demo scale | Low | DECIDED | FR-AI-011 |
| ARCH-DEC-007 | FIR document OCR | What technology for text extraction? | A: Catalyst Zia; B: Tesseract; C: PyPDF2 text-only | **C — PyPDF2 text-only** for MVP; image OCR Phase 2 | Low | DECIDED | FR-FIR-003 |

### Architecture Risks Register

| ARCH-RSK-ID | Risk | Probability | Impact | Mitigation |
|-------------|------|-------------|--------|-----------|
| ARCH-RSK-001 | AppSail unavailable or credits exhausted before demo | Medium | Very High | Test AppSail Day 1; have local Docker fallback |
| ARCH-RSK-002 | spaCy model download fails in AppSail environment | Medium | High | Bundle spaCy model into Docker image; use smaller model if needed |
| ARCH-RSK-003 | FAISS in-process uses too much RAM for AppSail tier | Low | Medium | Limit corpus to 2000 FIRs if memory constrained |
| ARCH-RSK-004 | Alembic migration fails on Catalyst Data Store | Medium | High | Test migration Day 1; have manual SQL fallback |
| ARCH-RSK-005 | 4-role migration breaks existing tests | Medium | Medium | Update test fixtures before running test suite |
| ARCH-RSK-006 | Stratus unavailable during upload demo | Low | Medium | Mock upload response with pre-stored hash |

### Architecture Open Questions

| ARCH-OQ-ID | Question | Target | Owner |
|-----------|---------|--------|-------|
| ARCH-OQ-001 | Does Catalyst AppSail support Python 3.11+ with scikit-learn and spaCy? | Day 1 | Backend Dev |
| ARCH-OQ-002 | What are the Catalyst Data Store table count and row limits for the hackathon project tier? | Day 1 | Backend Dev |
| ARCH-OQ-003 | Is Catalyst Zia's OCR service available in the hackathon tier? | Day 1 | Backend Dev |
| ARCH-OQ-004 | Does Catalyst Stratus support streaming multipart uploads? | Day 2 | Backend Dev |
| ARCH-OQ-005 | What is the Catalyst API Gateway request timeout? Does it affect long NER pipeline calls? | Day 1 | Backend Dev |

---

## 4. Principle Compliance Checklist

Use this checklist when reviewing any implementation decision or code change in Phase 2:

| # | Question | Principle |
|---|---------|-----------|
| 1 | Does this add a new deployable service unnecessarily? | PRINCIPLE-001, PRINCIPLE-016 |
| 2 | Does the frontend make an authorization decision alone? | PRINCIPLE-002, PRINCIPLE-003 |
| 3 | Does the backend apply role check + jurisdiction scope + field exclusion? | PRINCIPLE-003 |
| 4 | Does any AI output bypass the human review gate? | PRINCIPLE-004 |
| 5 | Does any RAG response lack a citation? | PRINCIPLE-005 |
| 6 | Is CasteRef/ReligionRef excluded at ORM SELECT level? | PRINCIPLE-006 |
| 7 | Is an audit event written before the response is returned? | PRINCIPLE-007 |
| 8 | Does the response schema include only fields needed for this operation? | PRINCIPLE-008 |
| 9 | Is file MIME type validated from content (not header)? | PRINCIPLE-009 |
| 10 | Is the seed data load idempotent? | PRINCIPLE-010 |
| 11 | Does AI failure isolate without crashing unrelated features? | PRINCIPLE-011 |
| 12 | Does every log entry include correlation ID and no sensitive data? | PRINCIPLE-012 |
| 13 | Does every P0 feature have a tested fallback path? | PRINCIPLE-013 |
| 14 | Is the new dependency Catalyst-compatible? | PRINCIPLE-014 |
| 15 | Is a synchronous call preferred over a new message queue? | PRINCIPLE-015 |

---

*End of 01-ARCHITECTURE-PRINCIPLES-AND-CONSTRAINTS.md*
