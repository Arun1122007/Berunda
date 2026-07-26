# 08 — Demo Story and Success Metrics

**Document ID:** BERUNDA-PH1-DEMO-001
**Version:** 1.0 | **Status:** APPROVED — Authoritative Phase 1 demo specification
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

> This document defines the exact demonstration sequence, the supporting data requirements,
> the failure fallbacks for each step, and the success metrics for the hackathon submission.
> No feature is included in the demo that is not in the approved P0 or P1 MVP scope.

---

## Part A — Demo Story

### Demo Premise

> **"Karnataka Police today operate with isolated FIR records. A suspect who appears in 5 cases across 3 districts looks like 5 unrelated files. Berunda solves this — converting raw FIR data into a connected, explainable, and auditable intelligence layer. In the next 5 minutes, I will show you how."**

The demo follows Inspector Ananya through the complete investigation workflow from FIR creation to graph-based hidden-link discovery, then switches to the state command and compliance views. All data is synthetic.

---

### Demo Personas Active During the Demonstration

| Demo User | Role | Dashboard Starts At |
|-----------|------|-------------------|
| ananya@demo | INVESTIGATOR — Bengaluru Urban, Electronic City Division | Investigator case list |
| priya@demo | SCRB_ANALYST — all districts | State command dashboard |
| krishna@demo | COMPLIANCE — all districts | Fairness and audit dashboard |

---

### Demo Steps

---

#### DEMO-STEP-01 — Login and Role-Specific Dashboard

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-01 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | Login screen → Investigator Dashboard |
| **Data Used** | ananya@demo credentials; Bengaluru Urban district scope |
| **Preconditions** | Demo environment provisioned; all 3 demo users created; seed data loaded |
| **Expected Visible Result** | After login, the investigator dashboard loads showing the case list scoped to Electronic City Division. The header shows "Bengaluru Urban — Electronic City Division". SYNTHETIC DATA banner is visible. |
| **Requirements Demonstrated** | FR-AUTH-001, FR-AUTH-003, FR-AUTH-004, NFR-PRV-003 |
| **Failure Fallback** | If login fails: clear browser cache; retry. If dashboard fails to load: switch to pre-recorded video. |
| **Narration Purpose** | Establishes that Berunda has authenticated, role-based access. Sets up the district-scoped workflow. |
| **Judge Value** | High — shows that access is controlled from the moment of login; no open access to all data |

---

#### DEMO-STEP-02 — Create FIR and Trigger AI Extraction

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-02 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | New FIR form (or document upload) → Extraction pending state |
| **Data Used** | Pre-prepared synthetic FIR document containing the phrase: "Accused Venkatesh Kumar (28) drove KA-01-AB-9999 to the Gold & Silver Shop, MG Road, Bengaluru on the night of 20 July 2026 and removed jewellery worth Rs. 4 lakhs." |
| **Preconditions** | Ananya is logged in; CrimeHead lookup table is populated |
| **Expected Visible Result** | (Option A — upload) Officer uploads the PDF. Progress indicator shows "Extracting entities from document…" (Option B — manual) Officer fills in the FIR form with BriefFacts text. After submit: success banner "FIR saved. AI extraction is running." CrimeNo is shown (e.g., BLR/ECD/2026/0051). |
| **Requirements Demonstrated** | FR-FIR-001, FR-FIR-002, FR-FIR-003, FR-AI-001, FR-AUD-001 |
| **Failure Fallback** | If upload fails: use manual form. If AI extraction fails: MockProvider activates; show MockProvider banner; extraction suggestions are pre-loaded mock values. |
| **Narration Purpose** | Shows the primary FIR creation workflow; introduces AI extraction. |
| **Judge Value** | Very High — this is the first functional step judges will evaluate |

---

#### DEMO-STEP-03 — Review and Approve AI Extraction

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-03 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | AI Extraction Review page |
| **Data Used** | Extraction result from DEMO-STEP-02: person "Venkatesh Kumar" (accused, 85% confidence), vehicle "KA-01-AB-9999" (91%), location "MG Road" (78%) |
| **Preconditions** | DEMO-STEP-02 completed; extraction result is available |
| **Expected Visible Result** | Extraction review page shows 3 cards: person, vehicle, location. Each card shows entity text, role, confidence percentage, and confidence colour (green for ≥ 80%, amber for 78%). "AI suggestion — review required" label is visible on each card. Officer edits vehicle registration to add a corrected variant if desired, then clicks Approve All. Success: "Entities saved. Entity resolution is running." |
| **Requirements Demonstrated** | FR-AI-002, FR-AI-003, FR-AI-004, NFR-AI-001, NFR-AI-002 |
| **Failure Fallback** | If extraction returned no results: use pre-loaded seed extraction result. If review UI fails to render: narrate that extraction happened and switch to DEMO-STEP-04. |
| **Narration Purpose** | Demonstrates responsible AI — officer reviews and corrects; nothing is saved without approval. |
| **Judge Value** | Very High — responsible AI with human review is a judging criterion |

---

#### DEMO-STEP-04 — Entity Resolution Surfaces Repeat Offender

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-04 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | Entity Resolution Review queue |
| **Data Used** | Seed data with planted repeat-offender: FIR-001 "Venkatesh Kumar", FIR-002 "Venkatesh Kumaar", FIR-003 "V. Kumar", FIR-004 "Venkatesha Kumar" — all in Electronic City Division. Merge candidate: confidence ≥ 0.80 with signals: phonetic name match, shared date-of-birth |
| **Preconditions** | Seed data loaded with planted patterns; entity resolution pipeline has run on seed data |
| **Expected Visible Result** | A badge in the navigation shows "3 entity merge suggestions pending". Officer opens the queue. Top candidate shows PersonA (FIR-001) and PersonB (FIR-003) side by side. Confidence: 83%. Signals: "Soundex match: VNTKSH, Date of birth: exact match". Officer clicks Approve. Success banner: "Merge approved. 4 cases are now linked to one resolved identity." |
| **Requirements Demonstrated** | FR-AI-005, FR-AI-006, FR-AI-007, AC-AI-005, AC-AI-006 |
| **Failure Fallback** | If entity resolution pipeline has not produced candidates: show candidate from seed data in queue (all demo data loaded in a single seed operation on Day 2); narrate that the engine produced this result in the background. |
| **Narration Purpose** | This is the signature technical capability — connecting the same person across 4 cases despite name variations. |
| **Judge Value** | Very High — directly addresses the core problem statement |

---

#### DEMO-STEP-05 — Relationship Graph and Profile View

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-05 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | PersonEntity profile → Relationship Graph view |
| **Data Used** | Canonical PersonEntity for Venkatesh Kumar with 4 linked cases, 2 co-accused, 1 linked vehicle (KA-01-AB-9999) |
| **Preconditions** | DEMO-STEP-04 completed; PersonEntity exists with 4 linked cases |
| **Expected Visible Result** | PersonEntity profile shows: Canonical name "Venkatesh Kumar", aliases (4 name variants), 4 linked cases with CrimeNos. Officer clicks "Relationship Graph". Force-directed graph renders with: 1 person node (orange), 4 case nodes (blue), 2 co-accused nodes (orange), 1 vehicle node (grey). Edges labelled with relationship types. |
| **Requirements Demonstrated** | FR-AI-007, FR-AI-008, NFR-PERF-003 |
| **Failure Fallback** | If graph renders blank: refresh; if still blank, show the profile view only and describe graph capability verbally. |
| **Narration Purpose** | Shows how Berunda makes the connection network visible. |
| **Judge Value** | Very High — visual impact; judges immediately understand the capability |

---

#### DEMO-STEP-06 — Hidden-Link Discovery

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-06 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | Relationship Graph — shortest-path query |
| **Data Used** | Case 001 and Case 042 connected via vehicle KA-01-AB-9999 (accused in Case 001 drove this vehicle; same vehicle appeared in Case 042 as a linked vehicle) |
| **Preconditions** | Graph is open; Case 001 and Case 042 nodes are visible or searchable |
| **Expected Visible Result** | Officer selects Case 001 node and Case 042 node, clicks "Find hidden link". Path is highlighted in the graph: Case 001 → [accused-drove] → Vehicle KA-01-AB-9999 → [vehicle-linked-to] → Case 042. Path panel shows the intermediate nodes and their relationship types. |
| **Requirements Demonstrated** | FR-AI-009, AC-GRAPH-002 |
| **Failure Fallback** | If BFS returns no path: narrate the expected result; show the path in the side panel from a pre-loaded graph result (computed during seed data load, not patched mid-demo). |
| **Narration Purpose** | The most visually dramatic moment — "two cases that seemed unrelated are actually connected." |
| **Judge Value** | Very High — peak demo moment; directly demonstrates the hidden-link discovery problem |

---

#### DEMO-STEP-07 — Hotspot Map and Anomaly Alert (SCRB Analyst View)

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-07 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | State Command Dashboard → Hotspot Map |
| **Data Used** | 5000-record synthetic dataset with planted 5× theft spike in Bengaluru Urban District, week 30 |
| **Preconditions** | priya@demo is logged in; seed data is loaded; anomaly detection has run |
| **Expected Visible Result** | Karnataka map renders with heatmap overlay. Bengaluru Urban district shows a red HIGH anomaly badge labelled "Theft: z-score 4.2 this week". Other districts show normal heatmap density. |
| **Requirements Demonstrated** | FR-RPT-001, FR-RPT-002, FR-RPT-003, FR-RPT-004, AC-MAP-001 |
| **Failure Fallback** | If map tiles fail to load: show the district table view (list of districts with case counts) as fallback. If anomaly badge is absent: narrate the detection and show the AnomalyAlert record from a database query. |
| **Narration Purpose** | Switches to supervisor/analyst perspective; shows state-wide situational awareness. |
| **Judge Value** | High — visually impactful; demonstrates analytics value for supervisors |

---

#### DEMO-STEP-08 — Anomaly Drill-Down

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-08 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | Hotspot Map → District drill-down → Case list |
| **Data Used** | Bengaluru Urban district; theft cases in week 30 |
| **Preconditions** | DEMO-STEP-07 completed; anomaly badge is visible |
| **Expected Visible Result** | Priya clicks the Bengaluru Urban anomaly badge. Side panel opens: "Bengaluru Urban — Theft spike: 47 cases this week vs. 9 cases baseline (z-score 4.2)". Contributing cases list shows CrimeNos. Priya clicks a CrimeNo — case detail opens. |
| **Requirements Demonstrated** | FR-RPT-002, FR-RPT-003, AC-MAP-002, AC-MAP-003 |
| **Failure Fallback** | If drill-down fails: show the case list filtered by district and crime type directly. |
| **Narration Purpose** | Demonstrates actionable intelligence — from state-level view to specific cases in seconds. |
| **Judge Value** | High — shows the analytical depth of the platform |

---

#### DEMO-STEP-09 — Explainable Risk Score

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-09 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | PersonEntity profile → Risk Score panel |
| **Data Used** | Venkatesh Kumar PersonEntity: 5 linked cases, most recent 10 days ago, 3 crime types — risk score > 0.75 |
| **Preconditions** | Risk scoring has run; Venkatesh Kumar PersonEntity has 4+ linked cases |
| **Expected Visible Result** | Risk score panel shows: score 0.82 — "HIGH". Feature importance bar chart shows top 5 features: (1) Number of prior cases — weight 0.41, (2) Days since last case — 0.29, (3) Crime type diversity — 0.18, (4) Average severity — 0.12, (5) Station frequency — 0.08. "Fairness verified" badge visible. CasteRef and ReligionRef are absent. |
| **Requirements Demonstrated** | FR-AI-013, FR-AI-014, FR-AI-015, AC-RISK-001 |
| **Failure Fallback** | If risk score is not computed: trigger manual recompute via Admin panel; if recompute fails, show the seed data score from the database directly (loaded during single seed operation on Day 2). |
| **Narration Purpose** | Shows responsible AI — explainable score, no protected characteristics. |
| **Judge Value** | Very High — explainability and fairness are explicit judging criteria |

---

#### DEMO-STEP-10 — Ask Berunda: Connection Query

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-10 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | Ask Berunda chat interface |
| **Data Used** | RAG corpus including FIR-001 and FIR-042; shared vehicle in both records |
| **Preconditions** | RAG corpus built; LLM provider available or MockProvider active |
| **Expected Visible Result** | Priya types: "What is the connection between FIR-001 and FIR-042?" Response: "FIR-001 (Jewellery Theft, MG Road, 20 Jul 2026) and FIR-042 (Vehicle Theft, Jayanagar, 18 Jun 2026) share vehicle registration KA-01-AB-9999. This vehicle was associated with the accused in FIR-001 and appeared as the stolen vehicle in FIR-042. [Sources: FIR-001, FIR-042]" Disclaimer visible below the answer. |
| **Requirements Demonstrated** | FR-AI-010, FR-AI-012, AC-RAG-001 |
| **Failure Fallback** | If LLM is unavailable: MockProvider provides a pre-scripted answer to this exact question. |
| **Narration Purpose** | Natural-language access to complex case data; most accessible demo feature for non-technical judges. |
| **Judge Value** | Very High — immediately demonstrates AI value to judges unfamiliar with data engineering |

---

#### DEMO-STEP-11 — Ask Berunda: Vehicle Case Query

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-11 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | Ask Berunda chat interface |
| **Data Used** | RAG corpus; vehicle KA-01-AB-9999 appears in 5 seeded cases |
| **Expected Visible Result** | Priya types: "What cases involve vehicle KA-01-AB-9999?" Response lists 5 FIR CrimeNos with brief descriptions. Citations show all 5 CrimeNos. |
| **Requirements Demonstrated** | FR-AI-010, FR-AI-012, AC-RAG-002 |
| **Failure Fallback** | MockProvider pre-scripted answer for vehicle query. |
| **Narration Purpose** | Shows the search-and-synthesise capability of the RAG system. |
| **Judge Value** | High |

---

#### DEMO-STEP-12 — Ask Berunda: Protected-Characteristic Refusal

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-12 |
| **Actor** | priya@demo (SCRB_ANALYST) |
| **Screen / Capability** | Ask Berunda chat interface |
| **Expected Visible Result** | Priya types: "What is Venkatesh Kumar's caste?" Response: "I cannot provide information on caste, religion, or other protected characteristics. Access to this data requires a Compliance role." No caste data is shown. |
| **Requirements Demonstrated** | FR-AUTH-005, AC-RAG-003, NFR-AI-001 |
| **Failure Fallback** | MockProvider returns the same pre-scripted refusal. |
| **Narration Purpose** | Demonstrates responsible AI and bias prevention. One of the most important governance moments in the demo. |
| **Judge Value** | Very High — responsible AI; anti-bias; fairness |

---

#### DEMO-STEP-13 — Fairness Dashboard (Compliance View)

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-13 |
| **Actor** | krishna@demo (COMPLIANCE) |
| **Screen / Capability** | Compliance Dashboard → Fairness Dashboard |
| **Data Used** | gov_FairnessCheckResult from the last model run |
| **Preconditions** | krishna@demo is logged in; fairness check has run |
| **Expected Visible Result** | Dashboard shows: Overall status: PASS (green). Per-model table: "Risk Score Model v1.0 — CasteID in features: No — ReligionID in features: No — Status: PASS". Feature importance table confirms top 5 features with no restricted characteristics. "View evidence" button shows full feature list. |
| **Requirements Demonstrated** | FR-AI-015, FR-AI-016, AC-FAIR-001, NFR-AI-003 |
| **Failure Fallback** | If fairness check has not run: trigger check via Admin panel; if dashboard fails, show the gov_FairnessCheckResult record from a direct database query. |
| **Narration Purpose** | The governance close — demonstrating that fairness is programmatically verifiable, not just claimed. |
| **Judge Value** | Very High — closing argument for responsible AI |

---

#### DEMO-STEP-14 — Audit Log Review

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-14 |
| **Actor** | krishna@demo (COMPLIANCE) |
| **Screen / Capability** | Audit Log view |
| **Data Used** | Audit events from the entire demo session |
| **Expected Visible Result** | Krishnamurthy filters audit log: date = today, user_id = ananya. Audit log shows: AUTH.LOGIN, FIR.CREATE, FIR.UPLOAD, AI.EXTRACTION.APPROVE (×3), ENTITY.MERGE.APPROVE, GRAPH.VIEW, GRAPH.SHORTESTPATH.QUERY, RAG.QUERY (×3). Each record shows timestamp, user ID, action, and resource ID. |
| **Requirements Demonstrated** | FR-AUD-001, FR-AUD-002, NFR-AUT-001, NFR-AUT-002, AC-AUD-001 |
| **Failure Fallback** | If audit log view is not yet implemented: show audit events via Admin panel debug view or raw DB query. |
| **Narration Purpose** | Closes the compliance loop — "every action Ananya took is permanently recorded." |
| **Judge Value** | High — accountability and audit trail are differentiating features |

---

#### DEMO-STEP-15 — Role Boundary Demonstration

| Field | Value |
|-------|-------|
| **Step ID** | DEMO-STEP-15 |
| **Actor** | ananya@demo (INVESTIGATOR) |
| **Screen / Capability** | Attempt to access Fairness Dashboard |
| **Expected Visible Result** | Ananya (logged in as INVESTIGATOR) attempts to navigate to /compliance/fairness. The application shows "Access denied — Compliance role required." HTTP 403 is returned by the API. |
| **Requirements Demonstrated** | FR-AUTH-003, AC-AUTH-006, NFR-SEC-003 |
| **Failure Fallback** | Show the 403 API response in browser developer tools if UI does not render the error message. |
| **Narration Purpose** | Final boundary check — "role-based access works in both directions." |
| **Judge Value** | Medium — confirms the security model is enforced |

---

### Closing Narration

> "In 5 minutes, you have seen: AI-assisted FIR capture with officer review gates, a repeat offender surfaced from 4 name variations, a hidden case link discovered through a shared vehicle, a live crime hotspot map with a detected anomaly, an explainable and fairness-verified risk score, plain-English case queries with citations, and a complete audit trail for every action — all running on Zoho Catalyst, on synthetic Karnataka Police data, with a 2-person team in 11 days. That is Project Berunda."

---

## Part B — Success Metrics

### Metric Conventions

- **[TARGET]** — proposed target, not yet measured; must be validated before Day 10
- **[CONSTRAINT]** — hard requirement that cannot be relaxed
- **[OBSERVED]** — will be measured during demo rehearsal and updated

---

### B1 — Product Success Metrics

| Metric ID | Metric | Target | Measurement Method |
|-----------|--------|--------|--------------------|
| PSM-001 | End-to-end demo workflow completes without manual patches | Zero manual patches required | Demo rehearsal on Day 10 |
| PSM-002 | P0 feature completion | 37/37 P0 features implemented | Feature checklist against scope baseline |
| PSM-003 | Role-specific dashboards correct for all 4 roles | 100% — all 4 roles show correct, scoped view | Login test for each demo user |
| PSM-004 | Protected-characteristic fields excluded from INVESTIGATOR and SCRB_ANALYST responses | 100% exclusion — 0 instances of CasteRef or ReligionRef in non-COMPLIANCE API responses | Automated API test |
| PSM-005 | Fairness check passes for all models before demo | 100% PASS | gov_FairnessCheckResult table |
| PSM-006 | All planted patterns discoverable in demo | All 5 AC-SEED-001 assertions pass | Seed validation test |

---

### B2 — Engineering Success Metrics

| Metric ID | Metric | Target | Measurement Method |
|-----------|--------|--------|--------------------|
| ESM-001 | Test coverage (unit + integration) | ≥ 70% for P0 feature code paths [TARGET] | `pytest --cov` report |
| ESM-002 | API P50 response time (data retrieval endpoints) | < 500 ms under demo load [TARGET] | Local load test with 5000-record dataset |
| ESM-003 | Global search response time (P95) | < 3 seconds for 5000 FIRs [TARGET] | Integration test timer |
| ESM-004 | Graph BFS computation time | < 5 seconds for 5000 nodes, 20000 edges [TARGET] | Integration test timer |
| ESM-005 | Audit event written for every P0 auditable action | 100% — 0 missing audit events for required event types | Integration test audit coverage check |
| ESM-006 | Zero crashed API endpoints during demo rehearsal | 0 unhandled exceptions in demo flow | Demo rehearsal run |
| ESM-007 | MockProvider activates within 5 seconds of AI service failure | < 5 seconds [TARGET] | Integration test |

---

### B3 — AI Evaluation Metrics

| Metric ID | Metric | Target | Measurement Method |
|-----------|--------|--------|--------------------|
| AEM-001 | NER extraction precision on synthetic FIR test set (person names) | ≥ 70% precision [TARGET] | Manually labelled 50-FIR test set |
| AEM-002 | NER extraction recall on synthetic FIR test set (person names) | ≥ 60% recall [TARGET] | Same test set |
| AEM-003 | Entity resolution planted repeat-offender detection | ≥ 3 of 4 FIR name variants merged into one PersonEntity | AC-AI-005 integration test |
| AEM-004 | RAG answer contains at least one citation per question | 100% — zero citation-less answers for rehearsed questions | Integration test of 3 rehearsed questions |
| AEM-005 | RAG protected-characteristic refusal | 100% — caste/religion questions always refused | Integration test of caste/religion queries |
| AEM-006 | Risk score excludes CasteRef and ReligionRef | 100% exclusion — fairness check PASS | gov_FairnessCheckResult record |
| AEM-007 | Risk score feature importance covers ≥ 4 of the 4 approved features | 100% — all 4 approved features appear in top 5 | Feature importance display test |

---

### B4 — Demo Success Metrics

| Metric ID | Metric | Target | Measurement Method |
|-----------|--------|--------|--------------------|
| DSM-001 | Demo completes all 15 steps without intervention | 15/15 steps completed in rehearsal | Rehearsal checklist |
| DSM-002 | Planted repeat-offender correctly surfaced | 1 PersonEntity with 4 linked cases visible in demo | DEMO-STEP-04 rehearsal |
| DSM-003 | Hidden link between Case 001 and Case 042 found | Path length ≤ 4 hops returned | DEMO-STEP-06 rehearsal |
| DSM-004 | Hotspot map anomaly badge visible for planted spike | Badge visible with z-score > 4.0 | DEMO-STEP-07 rehearsal |
| DSM-005 | Risk score with feature importance visible | Score and top 5 features displayed | DEMO-STEP-09 rehearsal |
| DSM-006 | Ask Berunda answers 3 rehearsed questions with citations | 3/3 answers include at least 1 citation | DEMO-STEP-10, 11, 12 rehearsal |
| DSM-007 | Fairness check shows PASS status | PASS indicator visible on dashboard | DEMO-STEP-13 rehearsal |
| DSM-008 | Pre-recorded fallback video exists and covers all 15 steps | Video file in archive/ | Manual check on Day 10 |

---

### B5 — Future Production Metrics

These are not hackathon targets. They are documented for the Phase 2 roadmap.

| Metric ID | Metric | Production Target |
|-----------|--------|------------------|
| FPM-001 | Investigator time to find cross-case connections | Reduced from hours to < 5 minutes per case |
| FPM-002 | FIR entity extraction recall with real police narratives | ≥ 80% (requires real annotated data) |
| FPM-003 | Entity resolution false-positive merge rate | < 5% (requires pilot feedback) |
| FPM-004 | Audit log coverage of sensitive data accesses | 100% (constraint — no reduction) |
| FPM-005 | Fairness check false-negative rate (protected-characteristic missed) | 0% (constraint) |
| FPM-006 | System uptime during working hours | ≥ 99% (requires production SLA) |

---

*End of 08-DEMO-STORY-AND-SUCCESS-METRICS.md*
