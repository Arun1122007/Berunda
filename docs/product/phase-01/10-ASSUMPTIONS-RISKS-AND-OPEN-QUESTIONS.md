# 10 — Assumptions, Risks, and Open Questions

**Document ID:** BERUNDA-PH1-ARQ-001
**Version:** 1.1 | **Status:** ACTIVE — Living document; updated after Phase 1 completion
**Classification:** INTERNAL | **Owner:** Berunda Team | **Last Updated:** 2026-07-26

> This register is the **active, authoritative** record of all Phase 1 assumptions, risks, decisions, and open questions.
> It supersedes `docs/discovery/CONTRADICTION_ASSUMPTION_AND_GAP_REGISTER.md` in scope.
> Do not silently remove entries. Mark resolved items as RESOLVED with evidence.

---

## Usage Convention

| Column | Guidance |
|--------|----------|
| ID | Stable identifier. Never reuse. |
| Status | OPEN / RESOLVED / ACCEPTED RISK / DEFERRED |
| Owner | Role or person responsible for validation |
| Evidence | File path or URL that supports the assumption |

---

## Part A — Assumptions Register

Assumptions are beliefs the team is acting on without complete proof. Each assumption carries a risk if incorrect.

| ASM-ID | Assumption | Why Required | Supporting Evidence | Risk if Wrong | Validation Method | Owner | Status |
|--------|-----------|-------------|--------------------|--------------|--------------------|-------|--------|
| ASM-001 | The Police FIR ER Diagram PDF (`blueprints/h2s/Police_FIR_ER_Diagram.pdf`) is the most recent authoritative version of the source schema | Schema design depends on ground truth; no other version found | PDF present in repo; cross-referenced with CATALYST_DATASTORE_SCHEMA_MAPPING.md | Schema drift between demo and actual ERD | Confirm with hackathon organiser that no newer ERD was released | Team | OPEN |
| ASM-002 | Catalyst QuickML currently supports LLM serving, RAG, and AutoML feature importance natively | Risk scoring and Ask Berunda features depend on QuickML | Blueprint sections 7-8 and 15 — NOT verified against live Catalyst docs | Architecture redesign required; may need to shift to external LLM only | Read help.catalyst.zoho.com QuickML section before Day 2 | Team | OPEN |
| ASM-003 | A 2-person team can complete the 12 MVP features in the remaining hackathon window | Determines scope | Implementation plan; timeline has elapsed; current feature status unknown | Scope must be cut; fallbacks needed | Complete a feature status review against IMPLEMENTATION_PLAN.md | Team | OPEN |
| ASM-004 | Synthetic data (Faker en_IN) is acceptable for judging | Demo depends on synthetic data | Blueprint design decision; Hack2Skill rules state synthetic is preferred | Demo data rejected; authenticity concerns | Confirm in challenge rules or with organiser | Team | OPEN |
| ASM-005 | Catalyst free tier / credits are sufficient for the demo at required scale | Deployment depends on credit availability | R003 mentions credit redemption; not verified against plan limits | Cost overrun or throttling during live demo | Log in to Catalyst console and check quota | Team | OPEN |
| ASM-006 | CasteID and ReligionID fields exist only on ComplainantDetails — **THIS ASSUMPTION IS INCORRECT** | Governance scope depends on which tables have these fields | ASSUMPTIONS.md A4 makes this claim — however CATALYST_DATASTORE_SCHEMA_MAPPING.md shows CasteRef and ReligionRef on Accused, Victim, AND ComplainantDetails | Governance scope is wider; RBAC and field-level security are under-specified | RESOLVED — update all governance docs to cover all three person-type tables | Team | RESOLVED (scope widened) |
| ASM-007 | BNS 2023 fully replaces IPC for crime category mapping purposes | Crime category mapping depends on legal basis | Resource acquisition notes; legal review not completed | Legal mapping may be premature; IPC-BNS transition is ongoing | Request legal guidance from organiser or flag as deferred | Team | OPEN |
| ASM-008 | Hackathon submission format is repository + demo video + slide deck | Day 11 deliverables depend on this | Discovery gap GAP-002; not confirmed by organiser | Day 11 preparation may be wrong; missing required deliverables | Check Hack2Skill Submissions tab for checklist | Team | OPEN |
| ASM-009 | OpenAI or Groq API keys are available for the demo environment | RAG and LLM features depend on a real LLM provider | Not verified | RAG falls back to MockProvider; demo quality affected | Confirm API key availability before Day 5 | Team | OPEN |
| ASM-010 | JWT-based authentication is sufficient for the MVP; SSO/OAuth is not required | Auth implementation depends on this decision | ASSUMPTIONS.md A7 | If organiser requires SSO, implementation must change | Confirm with organiser — for a hackathon demo, JWT is almost certainly acceptable | Team | ACCEPTED RISK |
| ASM-011 | NetworkX in-memory graph is sufficient for the 2000-5000 FIR demo dataset | Graph analytics depend on this scale assumption | Architecture validated for demo-scale; phase-1-validated-architecture.md section 8 | Graph operations too slow or OOM with larger datasets | Test with demo dataset size; if slow, reduce dataset or add caching | Dev | OPEN |
| ASM-012 | Catalyst Data Store supports the 35+ table schema without hitting table or row limits | Database design depends on this | Schema designed for Catalyst constraints; not verified at Catalyst console | Schema must be reduced or split | Verify Catalyst Data Store table and row limits before deploying schema | Team | OPEN |

---

## Part B — Risks Register

Risks are potential negative events that may affect the project. These are distinct from assumptions — they are known unknowns, not beliefs acted on.

| RSK-ID | Risk | Probability | Impact | Trigger | Mitigation | Contingency | Owner | Status |
|--------|------|-------------|--------|---------|------------|-------------|-------|--------|
| RSK-001 | Entity resolution algorithm is not implemented and may not be ready in time | High | High — core demo feature | Day 2-3 implementation window | Implement blocking + weighted scoring as specified in ADR-005 and ENTITY_RESOLUTION_SPECIFICATION.md | Fall back to showing manually seeded pre-matched entities; flag in demo as "match confirmed by officer" | Dev | OPEN |
| RSK-002 | Catalyst Functions scaffold is not implemented; production deployment blocked | High | High — deployment required for submission | Catalyst deployment attempted | Implement Node.js functions or use FastAPI + Ngrok / Catalyst AppSail as production equivalent | Use FastAPI locally as demo backend; document it as "local dev mode" with Catalyst architecture documented | Dev | OPEN |
| RSK-003 | QuickML capabilities do not match Blueprint assumptions (ASM-002) | Medium | High — affects risk scoring and RAG | Day 1 Catalyst investigation | Verify QuickML features on Day 1 | Use OpenAI directly for RAG; use scikit-learn directly for risk scoring on AppSail | Team | OPEN |
| RSK-004 | Demo breaks during live judging due to unverified data pipeline | Medium | Very High — directly affects score | Demo run on Day 10 | Full end-to-end rehearsal on Day 10; pre-recorded backup video | Switch to pre-recorded video mid-demo | Team | OPEN |
| RSK-005 | Catalyst Data Store not provisioned before Day 3 | Medium | High — all DB work blocked | Catalyst project setup | Redeem credits on Day 1; provision project immediately | Continue development against PostgreSQL locally; deploy schema on Day 5+ | Team | OPEN |
| RSK-006 | CasteID/ReligionID governance gap (ASM-006 RESOLVED) affects security implementation | Low (now resolved) | High — security flaw if not fixed | Security implementation begins | Update ASSUMPTIONS.md A4, ACCESS_CONTROL_MATRIX.md, and SECURITY_ARCHITECTURE.md before implementation | If not updated in time, block access to all Caste/Religion fields for all non-Compliance roles as a conservative fallback | Team | OPEN |
| RSK-007 | Scope creep — adding features beyond the 12 MVP items after Day 8 | Medium | Medium — jeopardises polish | Feature request after Day 8 | Enforce scope freeze per MVP_SCOPE_AND_RELEASE_PLAN.md Section 4 rule 1 | Defer all new features to STRETCH or VISION in backlog | Team | OPEN |
| RSK-008 | Submission format is not a live demo (e.g., only a video or slide deck required) | Low | Medium — changes Day 11 effort | Challenge rules checked | Confirm submission format immediately | Prepare both formats | Team | OPEN |
| RSK-009 | spaCy English NER performs poorly on Indian names and police narrative text | Medium | Medium — affects entity extraction quality | NER testing on synthetic data | Add custom entity patterns for Indian names and Indian vehicle numbers per AI_ML_SYSTEM_SPECIFICATION.md | Show extraction with confidence scores; note limitations in demo | Dev | OPEN |
| RSK-010 | Fairness check dashboard depends on QuickML feature importance being available | Medium | Medium — affects governance demo | QuickML verification | If QuickML not available, implement SHAP or simple feature coefficient display via scikit-learn | Display feature coefficient list as fairness evidence | Dev | OPEN |

---

## Part C — Open Questions

Open questions require a decision or external answer before the blocked work can proceed.

| OQ-ID | Question | Why It Matters | Blocked Work | Source | Target Answered By | Status |
|-------|---------|----------------|-------------|--------|-------------------|--------|
| OQ-001 | What is the exact submission format and deliverable checklist for the hackathon? | Determines Day 11 work; wrong format means disqualification | Day 11 plan | GAP-002 | Day 1 | OPEN |
| OQ-002 | Is there a list of mandatory Zoho Catalyst services for compliance scoring? | Guides Catalyst service mapping and feature decisions | Catalyst service selection | GAP-007 | Day 1 | OPEN |
| OQ-003 | Will real (sanitised) KSP data be provided, or must synthetic data be used exclusively? | Affects demo authenticity and data pipeline design | Data pipeline | GAP-005 | Day 1 | OPEN |
| OQ-004 | Is there a specific judging rubric or scoring criteria? | Guides polish priorities and feature cut decisions | Feature prioritisation | GAP-003 | Day 1 | OPEN |
| OQ-005 | Are there specific Catalyst resource limits for the hackathon (functions, rows, storage)? | Affects architecture scaling assumptions | Schema deployment, function design | GAP-007 | Day 1 | OPEN |
| OQ-006 | Does the hackathon require a live online demo or will a recorded video be accepted? | Determines whether Catalyst deployment is mandatory for submission or optional | Day 10-11 prep | ASM-008 | Day 1 | OPEN |
| OQ-007 | Which Catalyst authentication method should be used — Catalyst Auth (Zoho login) or custom JWT? | Authentication implementation depends on this | `apps/api/` auth implementation | ADR-009, SECURITY_ARCHITECTURE.md | Day 2 | OPEN |
| OQ-008 | Is Kannada NER a mandatory requirement or a stretch goal? | Affects Day 3-4 work allocation | NER pipeline scope | FR-006 (SHOULD, STRETCH) | Day 1 | OPEN |
| OQ-009 | Should the FIR document upload accept PDF, image, or structured CSV/Excel, or all three? | Determines upload pipeline design and OCR need | FIR upload use case (MISS-007) | Missing specification | Day 2 | OPEN |
| OQ-010 | What is the expected data volume for the demo — 200, 2000, or 5000 FIRs? | Affects synthetic data generation target and graph performance | Seed data script | MVP_SCOPE_AND_RELEASE_PLAN.md says 2000+; HACKATHON_DEMO_AND_PITCH_PLAN.md says 5000 | Day 1 | OPEN |

---

## Part D — Decisions Register

Decisions that have been made and recorded. These supplement the ADR list with product-level decisions not captured in architecture ADRs.

| DEC-ID | Decision | Rationale | Made By | Date | Source |
|--------|---------|-----------|---------|------|--------|
| DEC-001 | Phase 1 architectural style: Modular Functions + API Gateway | Not full microservices; Catalyst mandate | Team | 2026-07-17 | ADR-001 |
| DEC-002 | All services within a single Zoho Catalyst project | Catalyst deployment mandate | Team | 2026-07-17 | ADR-002 |
| DEC-003 | Berunda is an intelligence layer on top of CCTNS, not a replacement | Design scope boundary | Team | 2026-07-17 | ADR-003 |
| DEC-004 | Phase 1 graph: join tables not Neo4j | Neo4j not available on Catalyst | Team | 2026-07-17 | ADR-004 |
| DEC-005 | Entity resolution: rule-based blocking + weighted scoring | Neural matchers not feasible in 11 days | Team | 2026-07-17 | ADR-005 |
| DEC-006 | RAG output must be grounded; no hallucination mode | Public safety context; auditability | Team | 2026-07-17 | ADR-006 |
| DEC-007 | CasteID/ReligionID hard-excluded from all ML models | Responsible AI; fairness requirement | Team | 2026-07-17 | ADR-007 |
| DEC-008 | MVP is Phase 1 buildable features; Phases 2-6 are roadmap | Hackathon time constraint | Team | 2026-07-17 | ADR-008 |
| DEC-009 | Dual-language bootstrap: FastAPI local, Catalyst Functions production | Allows local dev without Catalyst SDK | Team | 2026-07-23 | ADR-009 |
| DEC-010 | Services and AI layer separated by contract | Architectural cleanliness; testability | Team | 2026-07-23 | ADR-010 |
| DEC-011 | Inline task execution (not Celery/Redis) for Phase 1 | Simplicity; Catalyst constraint | Team | 2026-07-23 | ADR-011 |
| DEC-012 | Single-tenant deployment; data access scoped by DistrictID | KSP organisational model | Team | 2026-07-23 | ASSUMPTIONS.md A2 |
| DEC-013 | All demo data is synthetic; no real PII in any environment | AGENTS.md safety rule; legal protection | Team | 2026-07-18 | AGENTS.md Rule 4 |
| DEC-014 | PostgreSQL 16 for production; SQLite permitted for local dev | Industry standard; Catalyst Data Store compatibility | Team | 2026-07-23 | ASSUMPTIONS.md A1 |
| DEC-015 | Audit log is append-only; no UPDATE or DELETE on gov_AuditLog | Audit compliance requirement | Team | 2026-07-23 | ASSUMPTIONS.md A9 |
| DEC-016 | 4 roles: INVESTIGATOR, SCRB_ANALYST, COMPLIANCE, ADMIN | Resolves CONFLICT-001; covers all stakeholder types | Phase 1 audit | 2026-07-26 | ACCESS_CONTROL_MATRIX.md |
| DEC-017 | FIR creation / upload / human verification workflow must be implemented as Priority 1 | Resolves CONFLICT-002; core hackathon demo requirement | Phase 1 audit | 2026-07-26 | This document |
| DEC-018 | CasteRef and ReligionRef governance scope must cover Accused, Victim, AND ComplainantDetails | Resolves CONFLICT-005; schema evidence | Phase 1 audit | 2026-07-26 | CATALYST_DATASTORE_SCHEMA_MAPPING.md |
| DEC-019 | Concurrent edit handling is not addressed in MVP | Last-write-wins default; no optimistic locking or conflict detection | Product decision (Phase 1 verification) | 2026-07-26 | PHASE-1-CORRECTION-PLAN.md §3 |

---

## Revision Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-07-26 | 1.0 | Initial creation from Phase 1 repository audit | Phase 1 audit |

---

*End of 10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md*
