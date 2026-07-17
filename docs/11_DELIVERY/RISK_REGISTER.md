# Risk Register

[//]: # (Document ID: BERUNDA-DEL-003 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Risk Table

| ID | Risk | Likelihood | Impact | Score | Mitigation | Contingency | Owner |
|----|------|-----------|--------|-------|------------|-------------|-------|
| R-001 | Entity resolution fails on planted test cases | MEDIUM | HIGH | HIGH | Test ER on Day 3 with planted data; tune thresholds | Skip ER demo, show pre-computed graph | Dev1 |
| R-002 | QuickML LLM unavailable during demo | LOW | CRITICAL | MEDIUM | Pre-compute answers; have backup screenshots | Show pre-recorded demo video | Dev1 |
| R-003 | Catalyst free-tier credit exhausted | MEDIUM | HIGH | HIGH | Monitor credit usage daily; optimize queries | Use local dev environment for demo | Both |
| R-004 | Team member unavailable (sick, emergency) | LOW | HIGH | MEDIUM | Cross-train on Day 1-2; document all code | Single person can deliver core features | Both |
| R-005 | Synthetic data generation has schema mismatch with Data Store | MEDIUM | HIGH | HIGH | Validate schema before generation; test import on Day 1 | Fix generator and re-run | Dev1 |
| R-006 | RAG hallucination during live demo | LOW | CRITICAL | MEDIUM | Use only pre-tested demo questions; citation verification | Pre-recorded demo as backup | Dev1 |
| R-007 | Performance: graph traversal too slow for demo | LOW | MEDIUM | LOW | Limit graph to 500 nodes for demo view; use cached results | Pre-compute graph for demo | Dev1 |
| R-008 | RBAC bug exposes restricted data | LOW | CRITICAL | MEDIUM | Automated RBAC tests in CI/CD; field-level access tests | Immediate fix + redeploy | Dev1 |
| R-009 | Catalyst Pipelines deployment failure | LOW | HIGH | MEDIUM | Test deployment flow on Day 1; document manual deploy steps | Manual deploy via Catalyst CLI | Dev2 |
| R-010 | Dashboard UI not rendering on demo machine | LOW | HIGH | MEDIUM | Cross-browser test (Chrome, Firefox, Edge) on Day 10 | Pre-loaded device with working demo | Dev2 |
| R-011 | Submission format unclear (GAP-002) | HIGH | HIGH | HIGH | Confirm with organizers by Day 5 | Prepare multiple formats (video, link, repo) | Both |
| R-012 | Judging rubric unavailable (GAP-003) | HIGH | MEDIUM | MEDIUM | Build demo to maximize feature breadth | Adjust focus based on rubric when available | Both |
| R-013 | Catalyst credits not redeemed (GAP-004) | HIGH | CRITICAL | CRITICAL | Redeem credits on Day 1 | Contact Catalyst support for emergency allocation | Dev1 |
| R-014 | QuickML capabilities insufficient (GAP-005) | MEDIUM | HIGH | HIGH | Verify QuickML docs by Day 2 | Fall back to local scikit-learn for risk scoring; template-based Q&A for RAG | Dev1 |
| R-015 | inv_arrestsurrenderaccused gap (GAP-001) | HIGH | LOW | LOW | Assume column structure per SOURCE_ERD_RECONCILIATION.md | Skip features that depend on this table; no MVP feature requires it | Dev1 |

## 2. Risk Response Priority

| Priority | Risks | Action |
|----------|-------|--------|
| CRITICAL | R-013 (credits), R-014 (QuickML) | Resolve by Day 2 |
| HIGH | R-001, R-003, R-005, R-008, R-011, R-015 | Mitigate by Day 5 |
| MEDIUM | R-002, R-004, R-006, R-007, R-009, R-010, R-012 | Contingency plan by Day 10 |

## 3. Risk Tracking

| Date | Risk ID | Status | Notes |
|------|---------|--------|-------|
| (To be updated during hackathon) | | | |
