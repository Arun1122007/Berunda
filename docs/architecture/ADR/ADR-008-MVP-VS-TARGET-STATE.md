# ADR-008: MVP vs Target State

[//]: # (Document ID: ADR-008 | Version: 1.0 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-17 | Review: Monthly)

---

## Context

The source documents describe a broad set of capabilities spanning from immediately buildable to far-future vision. The team has 11 days and 2 people. A clear scope boundary is needed to prevent scope creep.

## Decision

The MVP implements **only BUILDABLE-scope items**. STRETCH items are deferred (build if ahead of schedule). VISION items are documented as roadmap only — designed and described but not implemented.

| Scope | Action | Rule |
|-------|--------|------|
| ✅ BUILDABLE | Implement and demo | No exceptions |
| 🧩 STRETCH | Build only if Phase 1 is ahead of schedule | Default: defer |
| 🔭 VISION | Document in roadmap doc | Never build in hackathon |

### Frozen MVP Feature List

1. Synthetic FIR import/intake
2. English NER entity extraction from FIR narrative
3. Cross-case PersonEntity resolution with confidence + manual review
4. Case/person relationship graph and hidden-link demonstration
5. Geospatial hotspot map with temporal drill-down
6. Explainable risk scoring with prohibited-use controls
7. Anomaly/spike detection (z-score)
8. "Ask Berunda" grounded RAG over curated synthetic corpus
9. Authentication, RBAC, and jurisdiction boundary
10. Audit logging for sensitive reads and AI-assisted outputs
11. Live sensitive-feature exclusion/fairness control
12. Public-safe demo evidence pack

### Explicitly Deferred to STRETCH

Kannada NLP, MO fingerprinting, chain-of-custody hash, push notifications, OSM enrichment

### Explicitly Deferred to VISION

OSINT, cross-state correlation, Neo4j migration, event-driven architecture, ABAC, blockchain evidence anchoring, voice intake, multi-agent orchestration, 30-year backfill

## Rationale

- 12 BUILDABLE features is ambitious for 2 people in 11 days but achievable with the defined daily plan
- Adding STRETCH features risks jeopardizing core feature quality
- VISION features require legal clearance, data-sharing agreements, or platform capabilities not available in Phase 1
- Judges value a polished demo of fewer features over a broken demo of many features

## Consequences

- Positive: Clear scope boundary prevents last-minute feature creep
- Positive: Days 10-11 are protected for integration, testing, and demo prep
- Positive: Delivery risk is bounded
- Negative: Some differentiating features (Kannada NLP) may not be live in the demo
- Negative: Must clearly communicate "what's live vs roadmap" to judges

## Status

APPROVED
