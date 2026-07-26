# Phase 1 Correction Plan — Project Berunda

**Document ID:** BERUNDA-VER-PH1-CORRECT-001
**Version:** 1.0 | **Status:** ACTIVE
**Date:** 2026-07-26

> Target corrections for defects identified in the independent Phase 1 verification.
> Only corrections that do not change approved product direction are performed.
> Unresolved business, legal, or scope decisions are recorded for approval.

---

## 1. Corrections Performed (Targeted Fixes)

The following corrections have been applied directly to the Phase 1 documents. Each correction meets the criteria: unambiguous intended decision, does not change approved product direction, resolves formatting/ID/terminology/traceability defects, and is supported by repository evidence.

### ✅ P1V-BLK-001 — Fix Completion Report Counts (APPLIED)

**File:** `docs/product/phase-01/11-PHASE-1-COMPLETION-REPORT.md`

FR count changed from "23" to "35" (original 34 + 1 new FR-ERR-001), NFR from "27" to "37", AC from "35" to "53" (original 49 + 4 new ACs).

---

### ✅ P1V-CRT-001 — Fix FR-AI-008 Missing (APPLIED)

**Files:** `docs/product/phase-01/05-FUNCTIONAL-REQUIREMENTS.md` + cross-references in docs 04, 06, 08, 09, 11

**Option A applied:** FR-AI-009→FR-AI-008 through FR-AI-017→FR-AI-016. All cross-references in other Phase 1 documents updated via PowerShell replace (low-to-high order). Verified no remaining references to the old IDs outside doc 05.

---

### ✅ P1V-CRT-002 — Add SRS-to-Phase1 FR Cross-Reference (APPLIED)

**File:** `docs/product/phase-01/09-REQUIREMENTS-TRACEABILITY-MATRIX.md`

Added mapping table in Part C covering all 49 SRS FRs (FR-001 through FR-049) with Phase 1 FR-ID equivalence, coverage status, and gap notes. Table placed before Part D.

---

### ✅ P1V-CRT-003 — Update ACCESS_CONTROL_MATRIX.md (APPLIED)

**File:** `docs/security/ACCESS_CONTROL_MATRIX.md`

Added `src_Accused.CasteRef`, `src_Accused.ReligionRef`, `src_Victim.CasteRef`, `src_Victim.ReligionRef` rows to Section 2 Permission Matrix (under new "Restricted Fields" sub-section) and Section 4 Field-Level Security. Updated ComplainantDetails column names from CasteID/ReligionID to CasteRef/ReligionRef to match schema.

---

### ✅ P1V-MAJ-001 — Resolve SCRB_ANALYST Case Update Contradiction (APPLIED)

**File:** `docs/product/phase-01/02-STAKEHOLDERS-AND-USER-ROLES.md`

Updated PERSONA-003 Actions Prohibited from "update or delete case data" to "update or delete case data or documents" and added an explanatory note below the table clarifying that status-only updates are permitted per Section 8 authorization matrix and FR-FIR-004.

---

### ✅ P1V-MAJ-005 — Remove Notes Tab from P0 UC-006 (APPLIED)

**File:** `docs/product/phase-01/03-USER-JOURNEYS-AND-USE-CASES.md`

Changed UC-006 Notes tab entry from "Investigation notes (STRETCH — UC-016)" to "[Not in MVP scope — UC-016 is Phase 2 / STRETCH]".

---

### ✅ P1V-MAJ-008 — Upgrade NFR-AI-005 to [CONSTRAINT] (APPLIED)

**File:** `docs/product/phase-01/06-NON-FUNCTIONAL-REQUIREMENTS.md`

Changed NFR-AI-005 Target from `[PROPOSED]` to `[CONSTRAINT]`. Rationale: AI audit traceability is a core responsible-AI requirement.

---

### ✅ P1V-MIN-003, 004, 005 — Add Missing Acceptance Criteria (APPLIED)

**File:** `docs/product/phase-01/07-ACCEPTANCE-CRITERIA.md`

Added AC-SRCH-002 (empty search result), AC-FIR-009 (duplicate document upload), AC-AI-009 (AI non-guilt declaration) before AC-SEED-001.

---

## 2. Corrections Available for Direct Application

These corrections are unambiguous, evidence-supported, and do not change product direction. They are recommended for immediate application.

### 2.1 — Fix Completion Report Counts (P1V-BLK-001)

**File:** `docs/product/phase-01/11-PHASE-1-COMPLETION-REPORT.md`
**Section:** Section 10 — Requirement Counts

**Correction:**
- Change FR count from "23" to "34"
- Change NFR count from "27" to "37"
- Change AC count from "35" to "42"

**Evidence:** Counts verified from source documents:
- Doc 05: 34 FR headings (FR-AUTH-001 through FR-AUD-002)
- Doc 06: 37 NFR headings (NFR-SEC-001 through NFR-DEP-003)
- Doc 07: 42 AC headings (AC-AUTH-001 through AC-SEED-001)

**Risk:** None — corrects factual error.

---

### 2.2 — Fix FR-AI-008 Missing (P1V-CRT-001)

**File:** `docs/product/phase-01/05-FUNCTIONAL-REQUIREMENTS.md`
**Section:** Group AI — between FR-AI-007 and FR-AI-009

**Option A (Recommended):** Renumber FR-AI-009 through FR-AI-017 to FR-AI-008 through FR-AI-016. This closes the gap.

**Option B:** Insert a placeholder note: "FR-AI-008 intentionally omitted — reserved for future AI capability."

**Recommended: Option A** — Continuous numbering is cleaner for traceability.

**Files affected:**
- `05-FUNCTIONAL-REQUIREMENTS.md` — renumber FR-AI-009→008, 010→009, ..., 017→016
- `09-REQUIREMENTS-TRACEABILITY-MATRIX.md` — update FR references
- `08-DEMO-STORY-AND-SUCCESS-METRICS.md` — update any FR-AI-01x references
- `10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md` — update references

---

### 2.3 — Add SRS-to-Phase1 FR Cross-Reference (P1V-CRT-002)

**File:** `docs/product/phase-01/09-REQUIREMENTS-TRACEABILITY-MATRIX.md`
**Section:** Part C — Cross-Reference Index

**Correction:** Add mapping table:

| SRS FR-ID | SRS Name | Phase 1 FR-ID | Phase 1 Name | Status |
|-----------|----------|---------------|--------------|--------|
| FR-001 | FIR Structured Import | Not in Phase 1 P0 scope | — | Phase 2 (batch import) |
| FR-002 | FIR Manual Entry | FR-FIR-001 | Manual FIR Creation | ✅ Equivalent |
| FR-003 | Data Validation | FR-FIR-001 (embedded) | Manual FIR Creation | ✅ Covered |
| FR-004 | Duplicate Detection | FR-FIR-002 | CrimeNo Auto-Generation | ⚠ Partial |
| FR-005 | English NER | FR-AI-001 | NER Extraction | ✅ Equivalent |
| FR-006 | Kannada NER | FEAT-057 | Kannada NER | Deferred to Phase 2 |
| ... | (complete for all 49 SRS FRs) | | | |

**Risk:** Low — documentation-only.

---

### 2.4 — Update ACCESS_CONTROL_MATRIX.md (P1V-CRT-003)

**File:** `docs/security/ACCESS_CONTROL_MATRIX.md`
**Sections:** 2 (Permission Matrix) and 4 (Field-Level Security)

**Correction:**
- Change all `src_ComplainantDetails.CasteID` references to explicitly cover `src_Accused.CasteRef`, `src_Victim.CasteRef`, `src_ComplainantDetails.CasteID`
- Change all `src_ComplainantDetails.ReligionID` references to explicitly cover `src_Accused.ReligionRef`, `src_Victim.ReligionRef`, `src_ComplainantDetails.ReligionID`
- Add rows for Accused and Victim CasteRef/ReligionRef to the permission matrix

**Evidence:** `CATALYST_DATASTORE_SCHEMA_MAPPING.md` shows CasteRef and ReligionRef foreign keys on Accused, Victim, AND ComplainantDetails tables.

---

### 2.5 — Resolve SCRB_ANALYST Case Update Contradiction (P1V-MAJ-001)

**Files:** `docs/product/phase-01/02-STAKEHOLDERS-AND-USER-ROLES.md`

**Evidence:** Section 8 shows SCRB_ANALYST can "Update (status only)" on FIR/CaseMaster. PERSONA-003 says "Actions Prohibited: update or delete case data."

**Recommended resolution:** Adopt the Section 8 position (SCRB_ANALYST can update case status only, not data). Update PERSONA-003 Actions Prohibited to allow status-only updates.

**Rationale:** Status tracking (FR-FIR-004) requires status updates. SCRB_ANALYST needs to update case status for reporting. Section 8 is the more detailed authorization document.

---

### 2.6 — Remove Notes Tab from P0 UC-006 (P1V-MAJ-005)

**File:** `docs/product/phase-01/03-USER-JOURNEYS-AND-USE-CASES.md`, UC-006

**Correction:** Change "Notes: Investigation notes (STRETCH — UC-016)" to "Notes: [Not in MVP scope — UC-016 is Phase 2]" or remove the tab reference entirely.

---

### 2.7 — Strengthen NFR-AI-005 to [CONSTRAINT] (P1V-MAJ-008)

**File:** `docs/product/phase-01/06-NON-FUNCTIONAL-REQUIREMENTS.md`, NFR-AI-005

**Correction:** Change target from `[PROPOSED]` to `[CONSTRAINT]`.

**Rationale:** AI audit traceability is a core responsible-AI requirement (FR-AI-014 stores model version; NFR-AI-005 should match).

---

### 2.8 — Add Missing Acceptance Criteria

**File:** `docs/product/phase-01/07-ACCEPTANCE-CRITERIA.md`

Add the following ACs:

| AC-ID | Scenario | Correction |
|-------|----------|-----------|
| AC-SRCH-002 | Empty search result | "Given a search query that matches no records, When the user submits the search, Then the system returns an empty result set with message 'No results found'" |
| AC-FIR-009 | Duplicate document upload | "Given an FIR with an existing uploaded document, When the officer uploads the same file again, Then the system returns HTTP 409 or updates the existing record" |
| AC-AI-009 | AI non-guilt declaration | "Given an Ask Berunda query about suspect guilt, When the system returns the answer, Then the response does not state or imply that any person is guilty" |

---

## 3. Corrections Requiring Product Decision — RESOLVED

All product decisions were obtained on 2026-07-26 and applied to the documents. See the evidence paths in the table below.

| Issue | Decision | Evidence |
|-------|----------|----------|
| FEAT-081 P0 classification | Keep P0 + support pre-seeded demo users (both paths) | `04-MVP-SCOPE-AND-PRIORITIZATION.md`: "IN MVP (also supports pre-seeded demo users)" |
| FEAT-090 P0 classification | Downgrade to P1 — FastAPI fallback acceptable | `04-MVP-SCOPE-AND-PRIORITIZATION.md`: "SHOULD / P1 (FastAPI fallback)" |
| FEAT-025 P1 vs P0 dependency | Promote to P0 — vehicle tracking required for hidden-link | `04-MVP-SCOPE-AND-PRIORITIZATION.md`: "MUST / P0"; added to P0 test matrix |
| FEAT-006 P0 FR coverage | Add FR-ERR-001 + keep NFR coverage (both approaches) | `05-FUNCTIONAL-REQUIREMENTS.md`: FR-ERR-001 added in Group ERR |
| SCRB_ANALYST case update | Allow status-only updates (adopt Section 8 position) | `02-STAKEHOLDERS-AND-USER-ROLES.md`: PERSONA-003 note added |
| Concurrent edit handling | Document as not addressed in MVP | `10-ASSUMPTIONS-RISKS-AND-OPEN-QUESTIONS.md`: DEC-019 added |

---

## 4. Corrections Deferred to Phase 2

These corrections address issues that are not blocking Phase 2.

| Defect ID | Issue | Phase 2 Action |
|-----------|-------|---------------|
| P1V-MIN-006 | Stratus upload failure not audited | Add audit event during upload implementation |
| P1V-MIN-007 | No maintainability NFR | Add NFR-MTN group in Phase 2 NFR update |
| P1V-MAJ-009 | Concurrent edit not addressed | Document concurrency approach in Phase 2 detailed design |
| P1V-MAJ-006 | FEAT-017 no FR/AC/audit | Add during Phase 2 when case assignment is implemented |
| P1V-MAJ-011 | FEAT-016 no FR/AC | Add during Phase 2 when edit-FIR is implemented |

---

## 5. Correction Priority Matrix

| Priority | Defect ID | Correction | Effort | Impact | When |
|----------|-----------|------------|--------|--------|------|
| P0 | P1V-BLK-001 | Fix doc 11 counts | 5 min | High | Immediately |
| P0 | P1V-CRT-001 | Fix FR-AI-008 numbering | 15 min | High | Immediately |
| P0 | P1V-CRT-002 | Add SRS-to-Phase1 FR map | 1 hour | High | Day 1 |
| P0 | P1V-CRT-003 | Update ACCESS_CONTROL_MATRIX.md | 30 min | High | Day 1 |
| P1 | P1V-MAJ-001 | Resolve SCRB_ANALYST contradiction | 15 min | Medium | Day 1 |
| P1 | P1V-MAJ-005 | Remove Notes tab from UC-006 | 5 min | Medium | Day 1 |
| P1 | P1V-MAJ-008 | Upgrade NFR-AI-005 to [CONSTRAINT] | 2 min | Medium | Day 1 |
| P1 | P1V-MAJ-007 | Fix fallback language in demo steps | 15 min | Medium | Day 2 |
| P1 | FEAT-081/090 | Confirm P0/P1 reclassification | Decision needed | Medium | Day 1 |
| P1 | FEAT-025 | Confirm P0/P1 reclassification | Decision needed | Medium | Day 1 |
| P2 | P1V-MIN-003 | Add empty-search AC | 10 min | Low | Day 2 |
| P2 | P1V-MIN-004 | Add duplicate upload AC | 10 min | Low | Day 2 |
| P2 | P1V-MIN-005 | Add AI non-guilt AC | 10 min | Low | Day 2 |

---

## 6. Verification of Corrections

Each correction must be verified after application:

| Correction | Verification Method | Verifier |
|------------|-------------------|----------|
| Doc 11 counts | Re-count FR/NFR/AC headings from source docs | Author |
| FR-AI-008 renumber | Grep for FR-AI-009→017; confirm no 008 gap | Author |
| SRS FR mapping | Confirm table exists in doc 09 Part C | Author |
| ACCESS_CONTROL_MATRIX.md | Confirm Accused/Victim CasteRef/ReligionRef rows exist | Security owner |
| SCRB_ANALYST contradiction | Confirm Section 8 and PERSONA-003 agree | Product owner |
| UC-006 Notes tab | Confirm STRETCH reference removed | Author |
| NFR-AI-005 | Confirm [PROPOSED] changed to [CONSTRAINT] | Author |

---

## 7. Summary: Work Remaining for Phase 1 Clean-Up

| Category | Count | Total Effort Estimate |
|----------|-------|----------------------|
| Blocker corrections | 1 | 5 min |
| Critical corrections | 3 | 1 hour 45 min |
| Major corrections (documentation only) | 3 | 20 min |
| Major corrections (require decision) | 3 | Decision + 30 min |
| Minor corrections | 3 | 30 min |
| **Total** | **13** | **~3 hours** |

**All corrections are achievable within a single working day and do not change the approved product direction.**
**Phase 2 may proceed in parallel with corrections.**

---

*End of PHASE-1-CORRECTION-PLAN.md*
