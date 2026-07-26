# Phase 1 Traceability Reconstruction — Project Berunda

**Document ID:** BERUNDA-VER-PH1-TRACE-001
**Version:** 1.0 | **Status:** FINAL
**Date:** 2026-07-26

> This document independently reconstructs the traceability chain from problem through to verification method, comparing independent analysis against the existing RTM (doc 09). Gaps found in the existing RTM are flagged.

---

## 1. Methodology

The traceability chain follows: **Problem → Goal → Persona → Journey → Use Case → Feature → Functional Requirement → Non-Functional Requirement → Acceptance Criteria → Demo Step → Verification Method**.

Each row was independently constructed from source documents, then compared against the existing RTM (doc 09). Discrepancies are noted.

---

## 2. Full Traceability Chain

### AUTH — Authentication and Authorization

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.8 (No audit trail) | GOAL-008 | All | All | UC-001 | FEAT-001 | FR-AUTH-001 | NFR-SEC-001, 002, 003 | AC-AUTH-001, 002, 003, 004 | DEMO-STEP-01 | Integration test | ✅ |
| 3.8 | GOAL-008 | All | All | UC-001 | FEAT-005 | FR-AUTH-002 | NFR-SEC-003 | AC-AUTH-004 | DEMO-STEP-01 | Integration test | ✅ |
| Root cause (unauthorized access) | GOAL-008 | All | All | UC-001 | FEAT-002 | FR-AUTH-003 | NFR-SEC-003 | AC-AUTH-005, 006 | DEMO-STEP-01, 15 | Integration test | ✅ |
| Root cause (data leakage) | GOAL-008 | INVESTIGATOR | JOURNEY-001 | UC-001 | FEAT-003 | FR-AUTH-004 | NFR-PRV-001 | AC-AUTH-007, AC-MAP-004 | DEMO-STEP-01 | Integration test | ✅ |
| Root cause (protected-field exposure) | GOAL-008 | COMPLIANCE | JOURNEY-003 | UC-013 | FEAT-064 | FR-AUTH-005 | NFR-PRV-001 | AC-AUTH-008, 009 | DEMO-STEP-12, 13 | Integration test | ✅ |
| Operational requirement | GOAL-008 | ADMIN | Setup | UC-015 | FEAT-081 | FR-AUTH-006 | — | AC-USER-001, 002 | Demo setup | Integration test | ⚠ FEAT-081 P0 questioned |

### FIR — FIR Registration

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.1 (Unstructured FIR) | GOAL-001 | Ananya | JOURNEY-001 | UC-002 | FEAT-010 | FR-FIR-001 | — | AC-FIR-001, 002, 003, 004 | DEMO-STEP-02 | Integration test | ✅ |
| 3.1 | GOAL-001 | Ananya | JOURNEY-001 | UC-002 | FEAT-012 | FR-FIR-002 | NFR-INT-001 | AC-FIR-001 (CrimeNo format) | DEMO-STEP-02 | Integration test | ✅ |
| 3.1 | GOAL-001 | Ananya | JOURNEY-001 | UC-003 | FEAT-011 | FR-FIR-003 | NFR-INT-002 | AC-FIR-005, 006, 007, 008 | DEMO-STEP-02 | Integration test | ✅ |
| 3.6 (No structured investigation) | GOAL-001 | All | JOURNEY-001 | UC-002, UC-004 | FEAT-015 | FR-FIR-004 | — | (No dedicated AC — covered by AC-FIR-001 status check) | DEMO-STEP-03 | Integration test | ⚠ FEAT-015 AC coverage weak |
| 3.3 (Slow case retrieval) | GOAL-001 | Ananya | JOURNEY-001 | UC-006 | FEAT-013 | FR-FIR-005 | — | (No dedicated AC for FIR detail) | DEMO-STEP-02, 05 | Integration test | ⚠ FEAT-013 has no standalone AC |

### AI — Entity Extraction and Resolution

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.1, 3.2 | GOAL-001 | Ananya | JOURNEY-001 | UC-004 | FEAT-020 | FR-AI-001 | NFR-AI-001, 002 | AC-AI-001, AC-FIR-008 | DEMO-STEP-02, 03 | Integration test | ✅ |
| 3.2 | GOAL-001 | Ananya | JOURNEY-001 | UC-004 | FEAT-055 | FR-AI-002 | NFR-AI-001 | AC-AI-001 (confidence display) | DEMO-STEP-03 | UI test | ✅ |
| 3.2 | GOAL-001 | Ananya | JOURNEY-001 | UC-004 | FEAT-021 | FR-AI-003, 004 | NFR-AI-002 | AC-AI-002, 003, 004 | DEMO-STEP-03 | Integration test | ✅ |
| 3.4, 3.5 | GOAL-002 | Ananya | JOURNEY-001 | UC-007 | FEAT-022 | FR-AI-005 | NFR-AI-003 | AC-AI-005 | DEMO-STEP-04 | Integration test | ✅ |
| 3.4, 3.5 | GOAL-002 | Ananya | JOURNEY-001 | UC-007 | FEAT-023 | FR-AI-006 | — | AC-AI-006, 007, 008 | DEMO-STEP-04 | Integration test | ✅ |
| 3.5 | GOAL-002 | Ananya | JOURNEY-001 | UC-007 | FEAT-024 | FR-AI-007 | — | AC-AI-006 (linked cases) | DEMO-STEP-05 | Integration test | ✅ |

### GRAPH — Relationship Graph

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.4 | GOAL-003 | Ananya, Priya | JOURNEY-001, 002 | UC-008 | FEAT-030 | FR-AI-009 | NFR-PERF-003 | AC-GRAPH-001 | DEMO-STEP-05 | UI + Integration | ✅ |
| 3.4 | GOAL-003 | Ananya | JOURNEY-001 | UC-008 | FEAT-031 | FR-AI-010 | — | AC-GRAPH-002, 003 | DEMO-STEP-06 | Integration test | ✅ |

### ANALYTICS — Geospatial and Anomaly

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.7 | GOAL-004 | Ramesh, Priya | JOURNEY-002 | UC-009 | FEAT-040 | FR-RPT-001 | NFR-PERF-005 | AC-MAP-001 | DEMO-STEP-07 | UI test | ✅ |
| 3.7 | GOAL-004 | Ramesh, Priya | JOURNEY-002 | UC-009 | FEAT-041 | FR-RPT-002 | — | AC-MAP-002 | DEMO-STEP-07, 08 | UI test | ✅ |
| 3.7 | GOAL-004 | Ramesh, Priya | JOURNEY-002 | UC-009 | FEAT-042 | FR-RPT-003 | — | AC-MAP-003, 004 | DEMO-STEP-07 | UI test | ✅ |
| 3.7 | GOAL-006 | Ramesh, Priya | JOURNEY-002 | UC-011 | FEAT-043 | FR-RPT-004 | NFR-REL-002 | AC-MAP-001 (anomaly badge), AC-SEED-001 | DEMO-STEP-07, 08 | Integration test | ✅ |

### AI — Risk and Fairness

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.9 | GOAL-005 | Ananya, Priya | JOURNEY-001, 002 | UC-010 | FEAT-060 | FR-AI-014 | NFR-AI-003 | AC-RISK-001, 002, 003 | DEMO-STEP-09 | Integration test | ✅ |
| 3.9 | GOAL-005 | Ananya, Priya | JOURNEY-001, 002 | UC-010 | FEAT-061 | FR-AI-015 | — | AC-RISK-001 | DEMO-STEP-09 | UI test | ✅ |
| 3.8 | GOAL-008 | COMPLIANCE | JOURNEY-003 | UC-013 | FEAT-062 | FR-AI-016 | NFR-AI-003 | AC-FAIR-001, 003 | DEMO-STEP-13 | Integration test | ✅ |
| 3.8 | GOAL-008 | COMPLIANCE | JOURNEY-003 | UC-013 | FEAT-063 | FR-AI-017 | — | AC-FAIR-001, 002 | DEMO-STEP-13 | UI test | ✅ |

### AI — RAG

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.9 | GOAL-007 | Ananya, Priya | JOURNEY-001, 002 | UC-012 | FEAT-050 | FR-AI-011 | NFR-AI-004, 006 | AC-RAG-001, 002, 004 | DEMO-STEP-10, 11 | Integration test | ✅ |
| 3.9 | GOAL-007 | Ananya, Priya | JOURNEY-001, 002 | UC-012 | FEAT-054 | FR-AI-013 | NFR-AI-004 | AC-RAG-001, 002 | DEMO-STEP-10, 11 | Integration test | ✅ |
| 3.8 | GOAL-007 | Ananya, Priya | JOURNEY-001, 002 | UC-012 | FEAT-056 | FR-AI-012 | NFR-REL-001 | AC-RAG-005 | DEMO-STEP-10, 11, 12 | Integration test | ✅ |

### AUDIT — Audit and Governance

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| 3.8 | GOAL-008 | Krishnamurthy | JOURNEY-003 | UC-014 | FEAT-004 | FR-AUD-001 | NFR-AUT-001, 002, 003 | AC-AUD-001, 003 | DEMO-STEP-14 | Integration test | ✅ |
| 3.8 | GOAL-008 | Krishnamurthy | JOURNEY-003 | UC-014 | FEAT-080 | FR-AUD-002 | — | AC-AUD-001, 002 | DEMO-STEP-14 | Integration test | ✅ |

### INFRA — Infrastructure and Deployment

| Problem | Goal | Persona | Journey | UC | Feature | FR | NFR | AC | Demo Step | Verification | Status |
|---------|------|---------|---------|----|---------|----|-----|----|-----------|-------------|--------|
| Deployment | — | ADMIN | Setup | — | FEAT-090 | — | NFR-DEP-001 | — | Pre-demo | Deployment audit | ⚠ No FR, P0 questioned |
| Deployment | — | ADMIN | Setup | — | FEAT-091 | — | NFR-DEP-001 | — | Pre-demo | Schema deployment | ⚠ No FR |
| Demo data | — | ADMIN | Setup | — | FEAT-092 | — | NFR-REL-002 | AC-SEED-001 | Pre-demo | Seed validation | ✅ |

---

## 3. Gap Comparison: Independent Reconstruction vs. Existing RTM (Doc 09)

| Gap ID | Doc 09 Claim | Independent Finding | Verdict |
|--------|-------------|-------------------|---------|
| GAP-T01 | "All P0 features have ≥ 1 functional requirement" | FEAT-006, 081, 090 have no dedicated FRs | ⚠ OVERSTATED — Doc 09 Part B1 acknowledges this but claims "no P0 features are orphaned" |
| GAP-T02 | "All P0 features have acceptance criteria" | FEAT-013 has no standalone AC (covered implicitly by AC-FIR-001) | ⚠ PARTIALLY TRUE — AC coverage exists but indirectly |
| GAP-T03 | "12/12 traceability checks pass" | 12 checks pass but P0 FR coverage for FEAT-006, 081, 090 is acknowledged as "implicit" | ✅ Acceptable with documented exceptions |
| GAP-T04 | "No P0 gaps are unexplained" | FEAT-006 (Error handling) has no FR and no AC explicitly tagged to it | ⚠ P0 gap exists without dedicated spec |
| GAP-T05 | "Sensitive actions without audit: none" | Case assignment (FEAT-017) has no audit event | ⚠ P1 feature, acceptable |
| GAP-T06 | "No demo steps without requirements" | ✅ Confirmed — 15/15 demo steps have requirements | ✅ |

---

## 4. Orphan Features (Independent Analysis)

| Feature | Has FR? | Has AC? | Has NFR? | Has Demo Step? | Comments |
|---------|---------|---------|----------|----------------|----------|
| FEAT-006 (Error handling) | ❌ No FR | ❌ No dedicated AC | ✅ NFR-REL-003 | ⚠ All steps (implied) | NFR-only coverage |
| FEAT-007 (Health endpoint) | ❌ No FR | ❌ No AC | ✅ NFR-OBS-001 | ❌ No demo step | P1 — acceptable |
| FEAT-016 (Edit draft FIR) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-017 (Assign IO) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-025 (Vehicle tracking) | ❌ No FR | ❌ No AC | ❌ None | ⚠ DEMO-STEP-06 (implicit) | P1 — implied dependency |
| FEAT-026 (Location extraction) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-032 (Graph node expand) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-044 (Temporal trend charts) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-045 (State command dashboard) | ❌ No FR | ❌ No AC | ❌ None | ⚠ JOURNEY-002 (implicit) | P1 — orphaned |
| FEAT-046 (Crime category breakdown) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-051 (FIR summarisation) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-053 (Related-case recommendations) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-072 (Case timeline) | ❌ No FR | ❌ No AC | ❌ None | ❌ No demo step | P1 — orphaned |
| FEAT-081 (User management) | ✅ FR-AUTH-006 | ✅ AC-USER-001, 002 | ❌ None | ❌ Pre-demo only | P0 scope questioned |
| FEAT-090 (Catalyst Functions) | ❌ No FR | ❌ No AC | ✅ NFR-DEP-001 | ❌ Pre-demo | P0 scope questioned |
| FEAT-091 (Data Store schema) | ❌ No FR | ❌ No AC | ✅ NFR-DEP-001 | ❌ Pre-demo | P0 scope questioned |
| FEAT-092 (Seed data) | ❌ No FR | ✅ AC-SEED-001 | ✅ NFR-REL-002 | ❌ Pre-demo | ✅ AC covers it |

**Note:** All P1 features without FRs or ACs are acceptable per RTM B1 — they are deferred from detailed specification. However, FEAT-025, 026, and 045 have implicit dependencies from P0 demo steps, making their under-specification a risk.

---

## 5. Cross-Reference Integrity Check

| Check | Independent Result | Doc 09 Claim | Match? |
|-------|-------------------|-------------|--------|
| Problems → Goals | 9 problems → 8 goals | 9 problems → 8 goals | ✅ |
| Goals → Features | 8 goals → all have features | Same | ✅ |
| UC → Feature mapping | 15 MVP UCs → 30+ features | 15 MVP UCs → features | ✅ |
| Feature → FR | 37 P0 features → 34 FRs (3 implicit) | "All P0 features have FRs" | ⚠ Minor overstatement |
| FR → AC | 34 FRs → 42 ACs | 35 ACs claimed | ⚠ Count discrepancy |
| Demo step → FR | 15 steps → 25+ FRs | Same | ✅ |
| AI feature → review gate | 6 features → 6 gates | Same | ✅ |

---

## 6. Traceability Health Summary

| Metric | Value | Verdict |
|--------|-------|---------|
| Problems identified | 9 | ✅ |
| Goals defined | 8 | ✅ |
| Personas defined | 5 (4 primary + 1 admin) | ✅ |
| User journeys | 3 | ✅ |
| MVP use cases | 15 | ✅ |
| P0 features | 37 | ✅ (scope questioned for 2) |
| Functional requirements | 34 | ✅ |
| Non-functional requirements | 37 | ✅ |
| Acceptance criteria | 42 | ✅ |
| Demo steps | 15 | ✅ |
| Traceability gaps (P0) | 3 (FEAT-006, 081, 090 — documented) | ⚯ |
| Orphaned P1 features without FR/AC | 14 | ⚠ Acceptable for P1 |
| SRS-to-Phase1 FR mapping | 0 | ❌ Missing |

**Overall traceability reconstruction: PASS with conditions**

Conditions:
1. Add SRS-to-Phase1 FR cross-reference mapping
2. Document explicit FR for FEAT-006 or formally designate as NFR-only
3. Confirm P0 status for FEAT-081 and FEAT-090

---

*End of PHASE-1-TRACEABILITY-RECONSTRUCTION.md*
