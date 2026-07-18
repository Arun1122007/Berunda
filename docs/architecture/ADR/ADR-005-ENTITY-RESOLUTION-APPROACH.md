# ADR-005: Entity Resolution Approach

[//]: # (Document ID: ADR-005 | Version: 1.0 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-17 | Review: Monthly)

---

## Context

The source schema scopes Accused/Victim/Complainant records per-case with no native cross-case identity. Entity resolution must identify when multiple records refer to the same real person. The source documents propose a rule-based approach for Phase 1.

## Decision

**Phase 1:** Rule-based blocking + weighted similarity scoring.

- **Blocking:** Same district + age band (±3 years)
- **Features:** Name phonetic similarity (Soundex/Double Metaphone), name edit distance (Levenshtein), address overlap (token-based), age match
- **Weights:** Name phonetic 0.4, Name edit distance 0.3, Address overlap 0.2, Age match 0.1
- **Thresholds:** HIGH > 0.85 (auto-link), GREY 0.50-0.85 (manual review required), LOW < 0.50 (new entity)
- **Manual review:** UI presents possible matches for human confirmation

**Target State (Phase 3+):** Learned entity-resolution model (same approach used by OpenAleph/FollowTheMoney at OCCRP).

## Rationale

- Rule-based approach is transparent, debuggable, and sufficient for demo-scale data
- The planted "same person, 4 different names" test case is specifically designed to validate this approach
- Kannada/English name transliteration variance makes phonetic matching especially valuable
- Manual review for the grey zone maintains human-in-the-loop control
- Learned models require labeled training data that doesn't exist yet

## Consequences

- Positive: Transparent matching that can be explained to judges
- Positive: Works without labeled training data
- Positive: Manual review gate maintains human control
- Negative: Rule-based approach may miss subtle matches that a learned model would catch
- Negative: Threshold tuning requires experimentation against planted test data

## Status

APPROVED
