# Phase 10 & 11: Open Risks, Conditions, and Owners

**Document ID:** BERUNDA-REL-002  
**Version:** 2.0  
**Status:** ACTIVE — All items tracked to closure  
**Classification:** INTERNAL / RELEASE MANAGEMENT  
**Owner:** Berunda Team  
**Date:** 2026-07-27  
**Next Review:** 2026-07-28 (Daily Standup)

---

## 1. Risk and Condition Overview

| Severity | Count | Action Required |
|----------|-------|-----------------|
| 🔴 BLOCKER | 2 | Must resolve before demo |
| 🟠 HIGH | 3 | Strongly recommended before demo |
| 🟡 MEDIUM | 4 | Document fallback; resolve if time permits |
| 🟢 LOW | 4 | Resolve post-hackathon |

**Total Open Items: 13**

---

## 2. Blocker Risks (🔴)

### R-BLK-001: Backend AppSail 503 on Data Routes

| Field | Value |
|-------|-------|
| **Risk ID** | R-BLK-001 |
| **Title** | AppSail backend returns HTTP 503 on all data-access routes |
| **Description** | The Catalyst AppSail deployment at `https://berunda-api-50044292022.development.catalystappsail.in` responds correctly to `/health` (200) and `/ready` (200), but all data routes (e.g. `/api/v1/fir`, `/api/v1/auth/login`) return HTTP 503. This blocks the deployed frontend from retrieving or submitting data. |
| **Impact** | Deployed demo will show empty states or error screens for all data-driven features: FIR list, case detail, search, dashboard, AI review, reports |
| **Root Cause Hypothesis** | Possible causes: (1) AppSail runtime cannot connect to Catalyst Data Store; (2) MySQL/Data Store connection credentials incorrect in production environment; (3) AppSail package missing required dependencies; (4) Environment variables not propagated to AppSail runtime |
| **Symptoms** | `GET /health` → 200 OK; `GET /api/v1/fir` → 503 Service Unavailable |
| **Detection Method** | Post-deployment smoke tests (`TC-DEP-006` and beyond) |
| **Severity** | 🔴 BLOCKER |
| **Owner** | Deployment Team |
| **Deadline** | Day 10 (Hackathon Demo Day) |
| **Workaround** | Run demo entirely from local environment using SQLite + mock AI provider. Full 16-step flow verified locally. |
| **Resolution Path** | 1. Review AppSail deployment logs via Catalyst Console 2. Verify Data Store credentials in `.env.production` 3. Check Catalyst Data Store table existence via ZCQL 4. Run `deploy_schema_all.py` against production Data Store 5. Rebuild and redeploy AppSail package |
| **Verification** | `curl https://berunda-api-50044292022.development.catalystappsail.in/api/v1/fir` returns 200 with FIR array |

### R-BLK-002: Production AI Provider Keys Not Configured

| Field | Value |
|-------|-------|
| **Risk ID** | R-BLK-002 |
| **Title** | No production AI provider API keys provisioned for Zia LLM or OpenAI |
| **Description** | The AI extraction, summarization, and related-case generation features rely on a provider abstraction layer (`src/ai/providers/`). Without production API keys, the system falls back to `MockProvider`, which returns deterministic but unrealistic outputs. |
| **Impact** | Demo evaluators may question the realism of AI-generated FIR summaries and related-case suggestions. The `MockProvider` outputs are pre-defined strings that may not match actual case data. |
| **Mitigation** | `MockProvider` is verified to work correctly. For demo purposes, pre-generate AI outputs for the 16 demo steps and display them as "AI-generated" with a disclaimer. |
| **Severity** | 🔴 BLOCKER (for production AI demo) |
| **Owner** | AI Team |
| **Deadline** | Day 10 (for live AI demo) |
| **Workaround** | Use mock AI provider for demo; display pre-baked AI outputs matching demo cases |
| **Resolution Path** | 1. Request Zia LLM API credentials from Catalyst admin 2. Configure in `src/config.py` as `ZIA_API_KEY` 3. Test with `scripts/ai-evaluation/run_evaluation.py` 4. Alternatively, provision OpenAI key and configure `OPENAI_API_KEY` env var |
| **Verification** | `scripts/ai-evaluation/run_evaluation.py` returns PASS using production provider |

---

## 3. High Severity Risks (🟠)

### R-HGH-001: Catalyst Data Store Adapter Not Wired to Routes

| Field | Value |
|-------|-------|
| **Risk ID** | R-HGH-001 |
| **Title** | CatalystFIRRepository exists as isolated code — not injected into any router |
| **Description** | The repository pattern is defined with `CatalystFIRRepository` in `src/repositories/catalyst_adapter.py`, but all 24 routers in `src/routers/` use `AsyncSession = Depends(get_session)` directly. The production adapter is never called. |
| **Impact** | Even if AppSail 503 is fixed, the application queries SQLite, not the Catalyst Data Store. Data will not persist across AppSail restarts. |
| **Detection Method** | Code inspection in `docs/verification/02-datastore-access-audit.md` |
| **Severity** | 🟠 HIGH |
| **Owner** | Backend Team |
| **Deadline** | Post-hackathon |
| **Workaround** | AppSail SQLite file persists for session duration; acceptable for demo |
| **Resolution Path** | Refactor all routers to use repository injection from `src/dependencies.py`, selecting `CatalystFIRRepository` in production and `SQLiteFIRRepository` in development |

### R-HGH-002: Catalyst Free Tier Rate Limits During Demo

| Field | Value |
|-------|-------|
| **Risk ID** | R-HGH-002 |
| **Title** | High demo traffic may trigger Catalyst Development Tier rate limits |
| **Description** | The Catalyst Development Tier has unspecified rate limits on API calls, data store operations, and Stratus storage. A live demo with multiple evaluators walking through the 16-step flow simultaneously may hit these limits. |
| **Impact** | Rate-limited API calls return 429 or 503; demo flow breaks mid-presentation |
| **Detection Method** | Unknown — no monitoring dashboard for free tier |
| **Severity** | 🟠 HIGH |
| **Owner** | Deployment Team |
| **Deadline** | Day 9 |
| **Mitigation** | (1) Have local fallback environment ready on presenter machine; (2) Stagger evaluator sessions; (3) Minimize API calls per demo step by pre-loading data |
| **Resolution Path** | N/A — Catalyst Development Tier limitation. Mitigation only. |

### R-HGH-003: Schema Drift Between SQLite and Catalyst Data Store

| Field | Value |
|-------|-------|
| **Risk ID** | R-HGH-003 |
| **Title** | Alembic migrations target SQLite; Catalyst Data Store uses ZCQL schema definition |
| **Description** | The 8 alembic migrations in `src/alembic/versions/` use SQLAlchemy DDL compatible with SQLite. The Catalyst Data Store tables were defined via `deploy_schema_all.py` using ZCQL. These two schema definitions may diverge over time. |
| **Impact** | Demo data seeded locally via alembic may not match Catalyst Data Store schema; migration replay on Catalyst is impossible |
| **Detection Method** | Manual comparison of `src/models/` vs Catalyst table definitions |
| **Severity** | 🟠 HIGH |
| **Owner** | Database Team |
| **Deadline** | Post-hackathon |
| **Workaround** | Maintain SQLite as the source of truth; sync Catalyst tables manually |
| **Resolution Path** | Implement dual-target Alembic environment that can generate ZCQL-compatible DDL for Catalyst Data Store |

---

## 4. Medium Severity Risks (🟡)

### R-MED-001: Stratus File Upload Not Verified on Catalyst

| Field | Value |
|-------|-------|
| **Risk ID** | R-MED-001 |
| **Title** | Stratus bucket file upload has not been tested from AppSail runtime |
| **Description** | The Stratus storage design specifies 3 buckets (`berunda-data`, `berunda-artifacts`, `berunda-reports`) with MIME restrictions and 25MB limits. The `FileStorage` protocol has `LocalDiskStorage` and `CatalystStratusStorage` adapters, but the Catalyst adapter has not been tested end-to-end. |
| **Impact** | Evidence upload, report generation, and AI artifact storage may fail in production |
| **Severity** | 🟡 MEDIUM |
| **Owner** | Deployment Team |
| **Deadline** | Day 10 |
| **Workaround** | Demo can skip file upload steps or use local disk storage |

### R-MED-002: Frontend-Backend API Contract Discrepancies

| Field | Value |
|-------|-------|
| **Risk ID** | R-MED-002 |
| **Title** | Frontend API client may not match deployed backend's OpenAPI schema |
| **Description** | The frontend TypeScript API client in `apps/web/src/` was generated from a local OpenAPI schema. The deployed AppSail backend may serve a different schema if there are version mismatches. |
| **Impact** | API call failures, type mismatches, rendering errors on deployed frontend |
| **Severity** | 🟡 MEDIUM |
| **Owner** | Frontend Team |
| **Deadline** | Day 9 |
| **Workaround** | Pin frontend and backend to same commit hash for demo |

### R-MED-003: NVIDIA API Key Quota Exhaustion

| Field | Value |
|-------|-------|
| **Risk ID** | R-MED-003 |
| **Title** | NVIDIA API key (if used) quota exhaustion during demo |
| **Description** | If NVIDIA's API is used for any AI feature, the free tier quota may be exhausted during extended demo sessions. |
| **Mitigation** | Caching enabled in AI service layer; mock provider fallback available |
| **Severity** | 🟡 MEDIUM |
| **Owner** | AI Team |

### R-MED-004: Demo Script Relies on Specific Synthetic Data IDs

| Field | Value |
|-------|-------|
| **Risk ID** | R-MED-004 |
| **Title** | Demo script expects specific FIR IDs and case data that may differ between environments |
| **Description** | The 16-step demo flow references specific case numbers, person names, and evidence items. If the database is reseeded or if the Catalyst Data Store has different auto-increment IDs, the demo script will not match. |
| **Impact** | Presenter searches for a case ID that doesn't exist; demo flow breaks |
| **Severity** | 🟡 MEDIUM |
| **Owner** | QA Team |
| **Deadline** | Day 9 |
| **Workaround** | Take screenshots of all 16 demo steps from a known-good database state |

---

## 5. Low Severity Risks (🟢)

### R-LOW-001: No Playwright/Cypress Frontend E2E Tests

| Field | Value |
|-------|-------|
| **Risk ID** | R-LOW-001 |
| **Title** | Frontend has no automated browser-based E2E tests |
| **Description** | All 25 frontend tests are Vitest unit/integration tests. No Playwright or Cypress tests exist for browser-level verification. |
| **Impact** | UI regressions in routing, API call rendering, or error states may go undetected |
| **Severity** | 🟢 LOW |
| **Owner** | Frontend Team |
| **Deadline** | Post-hackathon |

### R-LOW-002: Quarantine Files Lack SHA256 Checksums

| Field | Value |
|-------|-------|
| **Risk ID** | R-LOW-002 |
| **Title** | Fetched resources in `data/quarantine/` have no integrity checksums |
| **Description** | 8 external resource files in `data/quarantine/` lack `.sha256` companion files. While the resources have non-zero sizes, their integrity cannot be cryptographically verified. |
| **Impact** | Low — resources are read-only reference copies |
| **Severity** | 🟢 LOW |
| **Owner** | Validation Team |
| **Deadline** | Post-hackathon |

### R-LOW-003: JSON Manifest Schema Differs from CSV

| Field | Value |
|-------|-------|
| **Risk ID** | R-LOW-003 |
| **Title** | `resource_manifest.json` (35 entries, R001 format) differs from `resource_manifest.csv` (92 entries, RSRC-001 format) |
| **Description** | The JSON manifest uses a different schema and resource ID format than the CSV manifest. This may cause confusion about which manifest is authoritative. |
| **Impact** | Low — both are valid for their respective use cases |
| **Severity** | 🟢 LOW |
| **Owner** | Validation Team |
| **Deadline** | Post-hackathon |

### R-LOW-004: `generate_synthetic.py` Lacks `--dry-run` Flag

| Field | Value |
|-------|-------|
| **Risk ID** | R-LOW-004 |
| **Title** | One Python acquisition script lacks consistent `--dry-run` flag |
| **Description** | Of 14 Python/PowerShell acquisition scripts, 13 support `--dry-run`. `generate_synthetic.py` does not. This is a consistency gap per the non-negotiable safety rules. |
| **Impact** | Low — generation is deterministic with seed-controlled output |
| **Severity** | 🟢 LOW |
| **Owner** | Validation Team |
| **Deadline** | Post-hackathon |

---

## 6. Previously Closed Risks

| ID | Title | Severity | Closure Date | Resolution |
|----|-------|----------|-------------|------------|
| R-P3-001 | Missing Repository Pattern in Async Routes | BLOCKER | 2026-07-26 | Refactored to async repository factories |
| R-P3-002 | Unsafe AI Extraction Fallback Provider | BLOCKER | 2026-07-26 | Secure offline synthetic extraction fallback |
| R-P3-003 | Evidence Storage Lacking Abstraction Layer | HIGH | 2026-07-26 | FileStorage protocol with adapters |
| R-P3-004 | Cross-Station Isolation Gaps | HIGH | 2026-07-26 | District-scoped subquery filtering |
| R-P3-005 | Missing Audit Events for State Mutations | HIGH | 2026-07-26 | 8 Phase 4 audit event types |
| R-P9-001 | Multi-station Authorization Boundary | HIGH | 2026-07-26 | Integration test suite verified |

---

## 7. Risk Tracking Metrics

| Metric | Value |
|--------|-------|
| Total open risks | 13 |
| Blocker (🔴) | 2 |
| High (🟠) | 3 |
| Medium (🟡) | 4 |
| Low (🟢) | 4 |
| Risks closed this phase | 6 |
| Risk closure rate | 6/19 (31.6%) |
| Mean time to resolution (closed) | ~3 days |
| Oldest open risk | R-BLK-001 (opened 2026-07-26) |

---

## 8. Escalation Path

| Severity | Response Time | Escalation To |
|----------|--------------|---------------|
| 🔴 BLOCKER | Immediate | Project Lead -> Hackathon Organizers |
| 🟠 HIGH | Within 4 hours | Project Lead |
| 🟡 MEDIUM | Within 24 hours | Technical Lead |
| 🟢 LOW | Next sprint | Team Lead |

---

## 9. Risk Review Schedule

- **Daily during Phase 12:** Standup review of all 🔴 and 🟠 items
- **Day 9 (Rehearsal):** Full dry-run of all 16 demo steps; verify workaround effectiveness
- **Day 10 (Demo):** Final risk check before presentation
- **Post-hackathon:** Move unresolved items to project backlog
