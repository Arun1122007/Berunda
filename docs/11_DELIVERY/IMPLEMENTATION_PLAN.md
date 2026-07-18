# Implementation Plan

[//]: # (Document ID: BERUNDA-DEL-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: All source documents | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Team

| Role | Person | Responsibilities |
|------|--------|------------------|
| Developer 1 (Backend + AI) | TBD | Data pipeline, NER, entity resolution, risk scoring, anomaly detection, RAG |
| Developer 2 (Frontend + Integration) | TBD | UI dashboard, graph viz, hotspot map, auth, audit, demo prep |

## 2. Day-by-Day Plan (11 Days)

### Day 1: Foundation

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Catalyst project setup + Data Store provisioning | Both | 2h | Catalyst project created, Data Store online |
| Generate synthetic data (v1: 500 FIRs) | Dev1 | 3h | SQL scripts for 500 FIRs |
| Import synthetic data | Dev1 | 1h | Data Store populated |
| Set up Catalyst Functions scaffolding | Dev1 | 2h | Function hello-world deployed |
| Set up React SPA scaffolding | Dev2 | 4h | Dashboard skeleton with routing |

### Day 2: Core Backend + Basic UI

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| FIR Ingestion Function (import + validate) | Dev1 | 4h | POST /cases/import working |
| Case list + detail API endpoints | Dev1 | 2h | GET /cases, GET /cases/{id} |
| Case list page + detail page UI | Dev2 | 4h | Case list + detail views functional |
| Catalyst Authentication integration | Dev2 | 2h | Login/logout working |

### Day 3: NER + Entity Resolution

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| NER extraction Function (spaCy) | Dev1 | 4h | NER extracts entities from BriefFacts |
| Entity Resolution Function (blocking + scoring) | Dev1 | 4h | ER logic with plant-4-names test passing |
| PersonEntity + PersonEntityLink tables populated | Dev1 | 2h | END-TO-END: import → NER → ER |
| Person search UI | Dev2 | 3h | Search by name, view linked cases |

### Day 4: Relationship Graph + Geospatial

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| RelationshipEdge discovery logic | Dev1 | 3h | Co-accused, accused-victim edges created |
| NetworkX shortest-path + degree centrality | Dev1 | 2h | Graph computation working |
| Cytoscape.js force-directed graph UI | Dev2 | 4h | Interactive graph with click-to-expand |
| Geospatial hotspot Function (KDE/hexbin) | Dev1 | 3h | Hotspot layer computed from Lat/Long |
| MapLibre GL hotspot map UI | Dev2 | 2h | Map with hexbin layer + district drill-down |

### Day 5: Anomaly Detection + Risk Scoring

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Anomaly detection Function (z-score) | Dev1 | 3h | Anomalies detected for planted spike |
| QuickML AutoML: train risk scoring model | Dev1 | 4h | Model trained on synthetic labeled data |
| Risk score computation + feature importance | Dev1 | 2h | RiskScore + RiskScoreFeatureImportance populated |
| Anomaly alert list UI | Dev2 | 2h | Alert list with severity indicators |
| Risk score explore UI (with feature importance chart) | Dev2 | 3h | Score + feature bar chart |

### Day 6: RAG + "Ask Berunda"

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| BriefFacts chunking + embedding | Dev1 | 3h | RAGCorpusChunk populated |
| RAG retrieval (vector similarity) Function | Dev1 | 3h | Top-K retrieval working |
| QuickML LLM integration for generation | Dev1 | 2h | End-to-end RAG working |
| RAG chat UI | Dev2 | 3h | Chat interface with citations display |

### Day 7: Auth, RBAC, Audit, Fairness

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| RBAC enforcement on all API endpoints | Dev1 | 3h | Role-based access working |
| Jurisdiction scoping for Investigator role | Dev1 | 2h | District-level filtering |
| Audit logging on all sensitive operations | Dev1 | 2h | gov_AuditLog populated correctly |
| Fairness check Function (FC-001 through FC-004) | Dev1 | 2h | FairnessCheckResult populated |
| Audit log viewer UI | Dev2 | 2h | Searchable audit log table |
| Fairness check dashboard UI | Dev2 | 2h | Check status display |

### Day 8: Integration + Polish

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Full synthetic dataset generation (5,000 FIRs) | Dev1 | 2h | Full dataset ready |
| End-to-end integration test | Both | 4h | All features work together |
| UI polish: loading states, error handling | Dev2 | 4h | Smooth UX |
| Caching layer for hotspot + analytics | Dev1 | 2h | Performance improvement |

### Day 9: Testing + Bug Fixing

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Security test suite (RBAC, injection, field access) | Dev1 | 3h | All security tests pass |
| Acceptance tests with planted data | Both | 4h | All AT-001 through AT-010 pass |
| Performance test (API latency under load) | Dev1 | 2h | p95 targets met |
| Bug fixes based on test results | Both | 3h | All critical bugs fixed |

### Day 10: Demo Prep

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Demo script rehearsal (5 iterations) | Both | 4h | Smooth 5-min demo |
| Demo evidence pack generation | Dev2 | 2h | Evidence pack PDF + screenshots |
| Pre-recorded 5-min demo video | Dev2 | 2h | Backup video |
| Slide deck finalization | Dev2 | 2h | Presentation ready |

### Day 11: Submission + Demo

| Task | Owner | Duration | Deliverable |
|------|-------|----------|-------------|
| Final smoke test | Both | 1h | All checks pass |
| Submission packaging | Dev2 | 2h | Submission package ready |
| Live demo (5 min + Q&A) | Both | 30 min | Demo delivered |
| Post-demo retrospective | Both | 1h | Lessons learned documented |

## 3. Critical Path

```
Day 1: Foundation
  └→ Day 2: Core Backend + UI
        └→ Day 3: NER + Entity Resolution (CRITICAL PATH)
              └→ Day 4: Graph + Geospatial
                    └→ Day 5: Anomaly + Risk
                          └→ Day 6: RAG
                                └→ Day 7: Auth + Audit
                                      └→ Day 8-9: Integration + Testing
                                            └→ Day 10-11: Demo
```

**Bottleneck:** Entity resolution (Day 3) is the most complex backend logic. If Day 3 slips, Days 4-11 compress accordingly.
