# Architecture Decision Record Index

[//]: # (Document ID: BERUNDA-ADR-IDX-001 | Version: 2.1 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-24 | Review: Monthly)

---

| ADR ID | Title | Decision | Status | Location |
|--------|-------|----------|--------|----------|
| ADR-001 | Phase 1 Architectural Style | Modular Functions + API Gateway; NOT full microservices or event-driven | APPROVED | `ADR/ADR-001-PHASE1-ARCHITECTURAL-STYLE.md` |
| ADR-002 | Catalyst Deployment Boundaries | All services within Catalyst; no external infrastructure dependencies | APPROVED | `ADR/ADR-002-CATALYST-DEPLOYMENT-BOUNDARIES.md` |
| ADR-003 | Source of Record vs Intelligence Layer | Separate schemas: source tables vs Berunda extension tables | APPROVED | `ADR/ADR-003-SOURCE-OF-RECORD-VS-INTELLIGENCE-LAYER.md` |
| ADR-004 | Graph Representation | Relational join tables (Phase 1); dedicated graph DB (Phase 3+) | APPROVED | `ADR/ADR-004-GRAPH-REPRESENTATION.md` |
| ADR-005 | Entity Resolution Approach | Rule-based blocking + weighted similarity (Phase 1); learned model (Phase 3+) | APPROVED | `ADR/ADR-005-ENTITY-RESOLUTION-APPROACH.md` |
| ADR-006 | RAG and Natural Language Query Safety | Retrieval-before-generation; parameterized templates; cited answers only | APPROVED | `ADR/ADR-006-RAG-AND-NATURAL-LANGUAGE-QUERY-SAFETY.md` |
| ADR-007 | Sensitive Field Exclusion | Hard exclusion of CasteID/ReligionID from all predictive models | APPROVED | `ADR/ADR-007-SENSITIVE-FIELD-EXCLUSION.md` |
| ADR-008 | MVP vs Target State | BUILDABLE scope only; STRETCH and VISION documented as roadmap | APPROVED | `ADR/ADR-008-MVP-VS-TARGET-STATE.md` |
| ADR-009 | Dual-Language Bootstrap Strategy | Python FastAPI for local dev; Node.js Catalyst Functions for production | APPROVED | `decisions/ADR-009-dual-language-bootstrap.md` |
| ADR-010 | Service-to-AI Separation Contract | Accept layering violation as Phase 1 debt; extract protocol interfaces in Phase 2 | APPROVED | `decisions/ADR-010-service-ai-separation-contract.md` |
| ADR-011 | Inline Task Execution Pattern | Replace Celery background tasks with direct inline async execution for Phase 1 | APPROVED | `decisions/ADR-011-inline-task-execution.md` |

## ADR Locations

Two ADR directories exist:

- `docs/architecture/ADR/` — ADR-001 through ADR-008 (Phase 1 architectural decisions)
- `docs/architecture/decisions/` — ADR-009 through ADR-011 (Phase 1 operational decisions)

Both are valid. Future ADRs should be placed in `docs/architecture/decisions/` to consolidate.
