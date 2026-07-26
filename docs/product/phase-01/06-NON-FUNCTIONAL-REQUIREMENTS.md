# 06 — Non-Functional Requirements

**Document ID:** BERUNDA-PH1-NFR-001
**Version:** 1.0 | **Status:** APPROVED — Phase 1 NFR baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> Targets marked **[PROPOSED]** are engineering targets to be validated by measurement.
> Targets marked **[CONSTRAINT]** are hard requirements derived from architecture decisions, legal obligations, or safety rules.
> No fake enterprise SLA guarantees are made. These are realistic hackathon targets.

---

## Group NFR-SEC — Security

### NFR-SEC-001 — Password Storage

**Requirement:** The system shall store user passwords as bcrypt hashes with a cost factor of at least 12. The system shall never log, transmit, or store a plaintext password. The system shall return HTTP 401 without revealing whether the username or the password was incorrect.

**Source:** SECURITY_ARCHITECTURE.md; standard practice
**Target:** [CONSTRAINT]
**Verification:** Code review — verify bcrypt usage; test that error message is generic

---

### NFR-SEC-002 — Transport Security

**Requirement:** The system shall require HTTPS for all API and web traffic in the demo environment. HTTP connections shall be redirected to HTTPS. The system shall reject connections using TLS < 1.2.

**Source:** SECURITY_ARCHITECTURE.md
**Target:** [CONSTRAINT]
**Verification:** Deployment check — verify HTTPS is enforced on Catalyst AppSail and Functions

---

### NFR-SEC-003 — JWT Security

**Requirement:** The system shall sign JWTs using HS256 with a secret key of at least 256 bits. The secret key shall be loaded from an environment variable and never committed to source control. The system shall validate the JWT signature, expiry, and role claim on every API request. The system shall reject tokens with missing or malformed claims with HTTP 401.

**Source:** ADR-009; SECURITY_ARCHITECTURE.md
**Target:** [CONSTRAINT]
**Verification:** Integration test — submit tampered JWT; verify 401; inspect secret key loading in code

---

### NFR-SEC-004 — Input Validation and Injection Prevention

**Requirement:** The system shall validate all user-supplied input at the API boundary using Pydantic schema validation. The system shall use parameterised ORM queries for all database access. The system shall not construct raw SQL strings from user input. The system shall sanitise file upload inputs by validating MIME type from file content, not from the filename or extension.

**Source:** OWASP Top 10; SECURITY_ARCHITECTURE.md
**Target:** [CONSTRAINT]
**Verification:** Code review — verify Pydantic schemas are applied to all endpoints; verify no raw SQL string construction; penetration test with SQL injection payload; verify MIME check from content

---

### NFR-SEC-005 — Environment Secret Management

**Requirement:** All sensitive configuration values (JWT secret, API keys, database credentials, Catalyst credentials) shall be loaded from environment variables. No secrets shall appear in source code, configuration files committed to version control, logs, or error messages. The `.env.example` file shall contain only placeholder values.

**Source:** AGENTS.md Rule 5; secrets-management.md
**Target:** [CONSTRAINT]
**Verification:** Git history check — grep for known secret patterns; code review of `.env.example`

---

### NFR-SEC-006 — Demo Environment Isolation

**Requirement:** The demo environment shall use a separate Catalyst project from any production instance (if applicable). Demo seed data shall be clearly labelled as SYNTHETIC in all API responses and UI displays. No real KSP data shall be loaded into the demo environment.

**Source:** AGENTS.md Rule 4
**Target:** [CONSTRAINT]
**Verification:** Manual check — verify all seed records contain SYNTHETIC label; verify no real PII in database

---

## Group NFR-PRV — Privacy

### NFR-PRV-001 — Protected-Characteristic Field Exclusion

**Requirement:** The system shall exclude `CasteRef` and `ReligionRef` from all API responses for INVESTIGATOR and SCRB_ANALYST roles. This exclusion shall be implemented at the ORM query level. The system shall verify in automated tests that these columns do not appear in response payloads for non-COMPLIANCE roles.

**Source:** ADR-007; CONFLICT-005 resolution; DEC-018
**Target:** [CONSTRAINT]
**Verification:** Automated test — request Accused record with INVESTIGATOR token; assert CasteRef and ReligionRef are absent from response JSON

---

### NFR-PRV-002 — Data Minimisation in API Responses

**Requirement:** The system shall return only fields required for the requested operation in each API response. The system shall not return all columns from all joined tables unless the endpoint specifically requires it. The system shall not include internal database IDs in publicly visible URLs without hashing or opaque identifiers.

**Source:** Privacy-by-design principle; PRIVACY_IMPACT_ASSESSMENT.md
**Target:** [PROPOSED]
**Verification:** Code review of response schemas; verify no oversized response objects

---

### NFR-PRV-003 — Synthetic Data Labelling

**Requirement:** All demo data records shall include a `data_source` field set to the value "SYNTHETIC". The system shall display a visible "SYNTHETIC DATA" banner on all case detail views and search result pages in the demo environment. The banner shall not be suppressed in any view.

**Source:** AGENTS.md Rule 4; SYNTHETIC_DATA_SPECIFICATION.md
**Target:** [CONSTRAINT]
**Verification:** UI test — verify banner visible on case detail; API test — verify data_source field value

---

## Group NFR-AUT — Auditability

### NFR-AUT-001 — Audit Log Immutability

**Requirement:** The system shall not provide any API endpoint that allows UPDATE or DELETE operations on `gov_AuditLog` records. The database application user (the user under which the backend connects to Catalyst Data Store) shall not have UPDATE or DELETE permissions on the `gov_AuditLog` table. Audit records shall be append-only.

**Source:** ASSUMPTIONS.md A9; AUDIT_LOGGING_AND_EVIDENCE_INTEGRITY.md; DEC-015
**Target:** [CONSTRAINT]
**Verification:** Attempt DELETE via API — verify HTTP 405; attempt DELETE at DB level — verify permission denied

---

### NFR-AUT-002 — Audit Event Completeness

**Requirement:** The system shall generate audit events for at minimum the following action categories: authentication (login, logout, failure), FIR lifecycle (create, upload, status change), AI events (extraction triggered, approved, rejected, edited, merge approved, merge rejected), data reads (case view, person view, risk score view), sensitive field access (CasteRef/ReligionRef access by COMPLIANCE or ADMIN), and administrative events (user create, role change). A missing audit event for any of these categories is a defect.

**Source:** FR-AUD-001; AUDIT_LOGGING_AND_EVIDENCE_INTEGRITY.md
**Target:** [CONSTRAINT]
**Verification:** Integration test sequence — perform each auditable action type; verify corresponding audit record exists

---

### NFR-AUT-003 — Audit Event Timing

**Requirement:** The system shall write the audit event before returning the HTTP response. If the audit write itself fails, the system shall log the failure to a local error log (not to stdout only) and shall still return the original API response. Audit write failure shall not block user operations but shall be reported in the system health endpoint.

**Source:** FR-AUD-001
**Target:** [PROPOSED]
**Verification:** Integration test — disable audit DB connection; submit an action; verify API response still returned; verify error appears in local log

---

## Group NFR-PERF — Performance

### NFR-PERF-001 — API Response Time (P50)

**Requirement:** The system shall return a P50 API response time of less than 500 ms for all standard data-retrieval endpoints (FIR detail, person profile, case list, search) under the demo load of 1 concurrent user and up to 5000 synthetic FIR records.

**Source:** Hackathon demo requirement — demo must not appear slow to judges
**Target:** [PROPOSED] — measurable via load test before Day 10
**Verification:** Local load test using `pytest-benchmark` or `locust` with 5000-record dataset; record P50 time

---

### NFR-PERF-002 — Search Response Time

**Requirement:** The system shall return search results for a global search query in less than 3 seconds for a corpus of up to 5000 FIR records with up to 10,000 person entities.

**Source:** FR-SRCH-001
**Target:** [PROPOSED]
**Verification:** Integration test — populate 5000 FIRs; run 20 search queries; measure response times; verify P95 < 3 seconds

---

### NFR-PERF-003 — Graph Computation Time

**Requirement:** The system shall build the in-memory NetworkX graph from the Data Store and compute a shortest-path BFS result in less than 5 seconds for a graph with up to 5000 nodes and 20,000 edges.

**Source:** ADR-004; UC-008
**Target:** [PROPOSED]
**Verification:** Integration test — build graph from 5000-record synthetic dataset; measure BFS computation time

---

### NFR-PERF-004 — Risk Score Batch Computation

**Requirement:** The system shall complete a full batch risk score computation for all resolved PersonEntities in less than 60 seconds for a dataset of up to 5000 FIRs and 3000 person entities.

**Source:** FR-AI-014
**Target:** [PROPOSED]
**Verification:** Integration test — trigger batch computation on full synthetic dataset; measure elapsed time

---

### NFR-PERF-005 — Map Tile and Heatmap Load Time

**Requirement:** The geospatial hotspot map with the heatmap overlay shall be fully rendered within 4 seconds of page load for a dataset of up to 5000 FIRs on a standard office internet connection (≥ 10 Mbps).

**Source:** FR-RPT-001; demo requirement
**Target:** [PROPOSED]
**Verification:** Browser performance test — measure map render time with 5000-record dataset

---

## Group NFR-REL — Reliability and Demo Resilience

### NFR-REL-001 — AI Service Fallback

**Requirement:** The system shall not present an unhandled error to the user when any AI service (LLM provider, NER service, embedding service) is unavailable. The system shall activate the MockProvider and display the limited-mode banner within 5 seconds of an AI service connection failure.

**Source:** FR-AI-012; demo resilience requirement
**Target:** [CONSTRAINT]
**Verification:** Integration test — invalidate LLM API key; submit RAG query; verify MockProvider activates and banner appears

---

### NFR-REL-002 — Demo Data Integrity

**Requirement:** The synthetic seed dataset shall contain all planted patterns required for the demo: at minimum 1 repeat-offender person entity resolvable across 4 FIRs, 1 hidden link discoverable via shortest-path BFS, 1 crime spike week detectable as z-score > 4.0, and 1 high-risk person entity with a risk score > 0.75. These patterns shall be validated by automated test before Day 10 rehearsal.

**Source:** DEMO-T04, DEMO-T06, DEMO-T08, DEMO-T09
**Target:** [CONSTRAINT]
**Verification:** Seed validation test — run planted-pattern assertions against loaded dataset; all 4 must pass

---

### NFR-REL-003 — Graceful Degradation

**Requirement:** If the Catalyst Data Store becomes unavailable, the system shall return HTTP 503 with a user-readable error message and shall not crash or restart. If any non-critical service (report generation, statutory counts) fails, the system shall return a partial response with the available data and a warning indicating which sections are unavailable.

**Source:** FEAT-006; hackathon demo reliability
**Target:** [PROPOSED]
**Verification:** Integration test — simulate DB connection failure; verify 503 returned; verify application process does not crash

---

### NFR-REL-004 — Demo Fallback Video

**Requirement:** A pre-recorded demo video covering all 15 DEMO-T test cases shall be produced by Day 10 and stored in `archive/demo-video-backup/`. The video shall be available as an immediate fallback if the live demo environment fails during judging.

**Source:** RSK-004 — demo breaks during live judging
**Target:** [CONSTRAINT — operational]
**Verification:** Manual check — confirm video file exists and covers all demo steps

---

## Group NFR-INT — Data Integrity

### NFR-INT-001 — CrimeNo Uniqueness

**Requirement:** The system shall enforce uniqueness of `CrimeNo` within the Data Store using a UNIQUE constraint on the `CaseMaster` table. The system shall not rely on application-layer uniqueness checks alone.

**Source:** FR-FIR-002
**Target:** [CONSTRAINT]
**Verification:** Integration test — attempt to insert duplicate CrimeNo at DB level; verify constraint violation

---

### NFR-INT-002 — File Hash Verification

**Requirement:** The system shall compute a SHA-256 hash of every uploaded file at upload time and store it in `EvidenceMaster`. On every subsequent download of the file, the system shall recompute the hash and compare it to the stored value. If hashes do not match, the system shall reject the download and write an `EVIDENCE.INTEGRITY_FAILURE` audit event.

**Source:** AUDIT_LOGGING_AND_EVIDENCE_INTEGRITY.md
**Target:** [PROPOSED — hash verification on download is a P1 feature]
**Verification:** Integration test — upload file; modify stored file in Stratus (simulated); download; verify rejection and audit event

---

### NFR-INT-003 — Audit Log Data Type Enforcement

**Requirement:** The system shall enforce the following data types on `gov_AuditLog`: event_id (UUID), event_type (enum), user_id (string), resource_id (string), timestamp (ISO 8601 UTC with timezone), district (string nullable), details (JSON). The system shall reject audit record insertions with invalid data types.

**Source:** FR-AUD-001
**Target:** [CONSTRAINT]
**Verification:** Schema verification test

---

## Group NFR-AI — AI Safety and Explainability

### NFR-AI-001 — AI Output Labelling

**Requirement:** Every AI-generated output presented to a user (NER extraction suggestion, risk score, RAG answer, FIR summary) shall be clearly labelled as AI-generated. The label "AI suggestion — review required" shall be visible adjacent to each AI output. The system shall not display AI output in a way that could be mistaken for an officially verified fact.

**Source:** ADR-006; responsible AI principles
**Target:** [CONSTRAINT]
**Verification:** UI review — verify label is present and visible on all AI output displays

---

### NFR-AI-002 — Human Review Gate

**Requirement:** The system shall not write any AI-extracted entity (person, vehicle, location) to a permanent database record without an explicit officer approval action. The system shall maintain AI suggestions in a temporary extraction queue until officer action is taken. AI suggestions shall not be auto-approved under any configuration setting in the MVP.

**Source:** ADR-006; DEC-006; product principle — Human Review First
**Target:** [CONSTRAINT]
**Verification:** Integration test — submit BriefFacts; verify extracted entities are not in permanent tables before officer approval; verify they appear after approval

---

### NFR-AI-003 — Protected-Characteristic Exclusion in ML

**Requirement:** The system shall verify, at model training time and before every batch scoring run, that CasteRef and ReligionRef are not in the model's feature list. This verification shall be implemented as a programmatic check (not a manual step) that blocks scoring if the check fails. The verification result shall be stored in `gov_FairnessCheckResult`.

**Source:** ADR-007; FR-AI-016
**Target:** [CONSTRAINT]
**Verification:** Integration test — inject CasteRef into feature list; verify scoring is blocked and FAIL result stored

---

### NFR-AI-004 — RAG Hallucination Prevention

**Requirement:** The system shall instruct the LLM (via the system prompt) to answer only based on the retrieved grounding documents. The system shall instruct the LLM to respond with "I do not have sufficient information in the case records to answer this question" when no relevant grounding content is available. The system shall not present a RAG answer without at least one citation.

**Source:** ADR-006; FR-AI-013
**Target:** [CONSTRAINT]
**Verification:** Integration test — submit question about a topic with no matching case records; verify grounding-insufficient response; verify no citation-less answers in rehearsed test questions

---

### NFR-AI-005 — AI Model Versioning and Traceability

**Requirement:** The system shall store the model version (a timestamp or hash of the training dataset and hyperparameter configuration) alongside every risk score record in `RiskScore.ModelVersion`. The system shall store the NER model version used alongside each extraction record in the extraction queue. This enables future audit queries to identify which model produced a specific output.

**Source:** MODEL_EVALUATION_AND_MLOPS_PLAN.md; responsible AI
**Target:** [PROPOSED]
**Verification:** Integration test — compute risk score; verify model version field is non-null in RiskScore record

---

### NFR-AI-006 — AI Authorization Scope Enforcement

**Requirement:** The RAG retrieval pipeline shall apply the authenticated user's jurisdiction scope when querying the corpus index. The system shall not retrieve or embed chunks from FIR records outside the INVESTIGATOR user's assigned stations. The system shall not permit a user to access AI outputs for records they are not authorised to view directly.

**Source:** FR-AI-011; UC-012; authorization-first principle
**Target:** [CONSTRAINT]
**Verification:** Integration test — load cases in two districts; authenticate as INVESTIGATOR in District A; submit RAG query; verify cited case IDs are only from District A

---

## Group NFR-OBS — Observability

### NFR-OBS-001 — Health Endpoint

**Requirement:** The system shall expose a `/health` endpoint that returns HTTP 200 with a JSON body containing: status ("ok" or "degraded"), database connectivity (boolean), AI provider status (reachable / mock / unavailable), and the application version string. The endpoint shall not require authentication.

**Source:** src/main.py existing health endpoint; FEAT-007
**Target:** [PROPOSED]
**Verification:** Manual check — call `/health` endpoint in deployed environment; verify all fields present

---

### NFR-OBS-002 — Structured Logging

**Requirement:** The system shall emit structured JSON logs to stdout for all request processing, including: request ID, endpoint, HTTP method, status code, processing time (ms), and user ID (if authenticated). The system shall not log plaintext passwords, JWT contents, or API keys.

**Source:** SECURITY_ARCHITECTURE.md; observability requirement
**Target:** [PROPOSED]
**Verification:** Run server; inspect log output; verify JSON format; verify no secrets in logs

---

## Group NFR-ACC — Accessibility and Browser Support

### NFR-ACC-001 — Browser Support

**Requirement:** The Berunda web application shall be functional in the latest stable versions of Google Chrome, Mozilla Firefox, and Microsoft Edge at the time of demo. The application shall not require browser plugins or extensions.

**Source:** React 18 web app; demo requirement
**Target:** [PROPOSED]
**Verification:** Manual test — run demo flow in Chrome, Firefox, and Edge; verify no functionality breaks

---

### NFR-ACC-002 — Responsive Layout

**Requirement:** The Berunda web application shall remain usable (no overlapping elements, no horizontal scroll) on screen resolutions from 1280×720 (minimum demo laptop resolution) to 2560×1440 (presenter screen). Full mobile-device optimization is not required in the MVP.

**Source:** Web app requirement; demo environment
**Target:** [PROPOSED]
**Verification:** Browser resize test — verify layout at minimum and maximum resolutions

---

## Group NFR-DEP — Deployment Constraints

### NFR-DEP-001 — Catalyst Architecture Compliance

**Requirement:** The production deployment shall use only Zoho Catalyst services. The system shall not depend on any infrastructure outside of the Catalyst project for the demo: API routing shall use Catalyst Functions or AppSail, data storage shall use Catalyst Data Store, file storage shall use Catalyst Stratus, authentication shall use Catalyst Auth or a JWT implementation hosted on AppSail.

**Source:** ADR-001; ADR-002; hackathon rules
**Target:** [CONSTRAINT]
**Verification:** Deployment audit — verify no external servers, no non-Catalyst databases, no non-Catalyst file storage in demo environment

---

### NFR-DEP-002 — No Real Production Data

**Requirement:** The demo environment shall not contain any real police record data, real personal information, real vehicle information, or any data obtained without explicit data-sharing agreement. All data in the demo environment shall be synthetically generated using Faker en_IN or similar tools.

**Source:** AGENTS.md Rule 4; DEC-013
**Target:** [CONSTRAINT]
**Verification:** Manual data audit — sample 20 records; verify all names, addresses, phone numbers, and registration numbers are synthetic

---

### NFR-DEP-003 — Demo Stability After Data Load

**Requirement:** After the synthetic seed data is loaded and the demo environment is provisioned, the system shall not require any manual data patches, script executions, or database modifications to complete the demo flow. All planted patterns shall be loadable in a single seed operation.

**Source:** SRSK-007 — demo rehearsal must complete without patches
**Target:** [CONSTRAINT]
**Verification:** Full end-to-end demo rehearsal on Day 10 without any manual interventions

---

*End of 06-NON-FUNCTIONAL-REQUIREMENTS.md*
