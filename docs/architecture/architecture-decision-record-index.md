# Architecture Decision Record Index

[//]: # (Document ID: BERUNDA-ADR-IDX-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Architects, Team Lead | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-17 | Review: Monthly)

---

| ADR ID | Title | Decision | Status |
|--------|-------|----------|--------|
| ADR-001 | Phase 1 Architectural Style | Modular Functions + API Gateway; NOT full microservices or event-driven | APPROVED |
| ADR-002 | Catalyst Deployment Boundaries | All services within Catalyst; no external infrastructure dependencies | APPROVED |
| ADR-003 | Source of Record vs Intelligence Layer | Separate schemas: source tables vs Berunda extension tables | APPROVED |
| ADR-004 | Graph Representation | Relational join tables (Phase 1); dedicated graph DB (Phase 3+) | APPROVED |
| ADR-005 | Entity Resolution Approach | Rule-based blocking + weighted similarity (Phase 1); learned model (Phase 3+) | APPROVED |
| ADR-006 | RAG and Natural Language Query Safety | Retrieval-before-generation; parameterized templates; cited answers only | APPROVED |
| ADR-007 | Sensitive Field Exclusion | Hard exclusion of CasteID/ReligionID from all predictive models | APPROVED |
| ADR-008 | MVP vs Target State | BUILDABLE scope only; STRETCH and VISION documented as roadmap | APPROVED |

## ADR Location

All ADR documents are in `docs/architecture/ADR/` with filenames matching the format `ADR-NNN-TITLE.md`.
