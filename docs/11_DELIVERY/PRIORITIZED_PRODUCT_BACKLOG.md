# Prioritized Product Backlog

[//]: # (Document ID: BERUNDA-DEL-002 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team, Product | Source: All source documents | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. MVP Backlog (Must Have — BUILDABLE)

| Rank | ID | Feature | Effort (person-days) | Dependencies | SRS Reference |
|------|-----|---------|---------------------|--------------|---------------|
| 1 | B-001 | Catalyst project setup + Data Store | 0.5 | None | FR-001 |
| 2 | B-002 | Synthetic data generator (5,000 FIRs) | 1 | B-001 | FR-001 |
| 3 | B-003 | FIR Ingestion Function (import + validate) | 1 | B-001, B-002 | FR-001, FR-003, FR-004 |
| 4 | B-004 | Case list + detail API | 0.5 | B-003 | FR-001 |
| 5 | B-005 | React dashboard skeleton + case pages | 1.5 | B-004 | — |
| 6 | B-006 | Catalyst Authentication integration | 0.5 | B-005 | FR-035 |
| 7 | B-007 | NER extraction Function (spaCy) | 1 | B-003 | FR-005, FR-007, FR-008 |
| 8 | B-008 | Entity Resolution Function (blocking + scoring) | 1 | B-007 | FR-009, FR-010, FR-011, FR-012 |
| 9 | B-009 | Person search + view UI | 1 | B-005, B-008 | FR-009 |
| 10 | B-010 | Manual merge review UI | 0.5 | B-009 | FR-013, FR-014, FR-015 |
| 11 | B-011 | RelationshipEdge discovery | 0.5 | B-008 | FR-016 |
| 12 | B-012 | NetworkX graph computation (shortest-path, centrality) | 0.5 | B-011 | FR-017 |
| 13 | B-013 | Cytoscape.js relationship graph UI | 1 | B-012 | FR-018 |
| 14 | B-014 | Geospatial hotspot Function (KDE/hexbin) | 1 | B-003 | FR-021 |
| 15 | B-015 | MapLibre GL hotspot map UI | 1 | B-014 | FR-021, FR-022 |
| 16 | B-016 | Temporal + jurisdiction filter | 0.5 | B-015 | FR-023 |
| 17 | B-017 | Anomaly detection Function (z-score) | 0.5 | B-003 | FR-024, FR-025 |
| 18 | B-018 | Anomaly alert list UI | 0.5 | B-017 | FR-025 |
| 19 | B-019 | QuickML AutoML: train risk scoring model | 1 | B-008 | FR-026 |
| 20 | B-020 | Risk score computation + feature importance | 0.5 | B-019 | FR-027, FR-028, FR-029 |
| 21 | B-021 | Risk score explorer UI | 1 | B-020 | FR-029 |
| 22 | B-022 | RAG corpus chunking + embedding | 1 | B-003 | FR-030 |
| 23 | B-023 | RAG retrieval + LLM generation Function | 1 | B-022 | FR-030, FR-031 |
| 24 | B-024 | "Ask Berunda" chat UI | 1 | B-023 | FR-030, FR-031, FR-032, FR-033 |
| 25 | B-025 | RBAC enforcement on all endpoints | 1 | B-006 | FR-036, FR-037 |
| 26 | B-026 | Jurisdiction scoping filter | 0.5 | B-025 | FR-037 |
| 27 | B-027 | Audit logging on all sensitive ops | 1 | B-025 | FR-039, FR-040, FR-041, FR-042 |
| 28 | B-028 | Audit log viewer UI | 0.5 | B-027 | FR-042 |
| 29 | B-029 | Fairness check Function | 0.5 | B-020 | FR-043, AIR-009 |
| 30 | B-030 | Fairness check dashboard UI | 0.5 | B-029 | FR-043 |
| 31 | B-031 | Synthetic data labeling (watermark + tag) | 0.5 | B-002 | — |
| 32 | B-032 | Health check + system info endpoint | 0.25 | B-001 | — |

**Total MVP effort:** ~22.75 person-days (2 persons × 11 days = 22 person-days available)

## 2. STRETCH Backlog

| Rank | ID | Feature | Effort | Dependencies |
|------|-----|---------|--------|--------------|
| S-001 | S-001 | Kannada NER with indic-faker | 2 | B-007 |
| S-002 | S-002 | MO pattern matching (embedding similarity) | 1.5 | B-003, B-007 |
| S-003 | S-003 | Vehicle link UI | 0.5 | B-007 |
| S-004 | S-004 | Chain-of-custody SHA-256 hash on audit log | 1 | B-027 |
| S-005 | S-005 | OpenStreetMap enrichment | 1.5 | B-015 |

## 3. VISION Backlog (Documented, Not Built)

| ID | Feature | Phase |
|-----|---------|-------|
| V-001 | Kannada NLP full | Phase 2 |
| V-002 | OSINT integration | Phase 3 |
| V-003 | Cross-state correlation | Phase 3 |
| V-004 | Neo4j graph database migration | Phase 3 |
| V-005 | Event-driven architecture (Catalyst Signals) | Phase 3 |
| V-006 | ABAC (Attribute-Based Access Control) | Phase 3 |
| V-007 | Blockchain evidence anchoring | Phase 4 |
| V-008 | Voice-based FIR intake | Phase 4 |
| V-009 | Multi-agent AI orchestration | Phase 4 |
| V-010 | 30-year historical data backfill | Phase 4 |
