# MVP Scope and Release Plan

[//]: # (Document ID: BERUNDA-MVP-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint + 03_Implementation_Plan | Last Verified: 2026-07-17 | Review: Monthly)

---

## MVP Definition

The Berunda MVP is a working, demoable slice that touches every architectural layer — data ingestion, entity resolution, AI scoring, geospatial analytics, relationship graphs, natural-language query, security, and governance. It is not a mockup.

## MVP Feature Set (Frozen)

| # | Feature | Acceptance Criteria | Demo Evidence |
|---|---------|-------------------|---------------|
| 1 | Synthetic FIR import | 2000+ synthetic FIRs loaded into Data Store with referential integrity | Dashboard shows case list with synthetic data |
| 2 | English NER extraction | NER entity extraction from BriefFacts outputs persons, locations, vehicles with confidence scores | FIR detail shows extracted entities |
| 3 | Cross-case entity resolution | Planted repeat-offender (4 cases, 4 different names/ages) resolved to single PersonEntity | Entity resolution match visible with confidence score |
| 4 | Relationship graph | Clicking a PersonEntity shows force-directed graph with linked cases, co-accused, vehicles | Graph renders with edge thickness = confidence |
| 5 | Geospatial hotspot map | Hexbin layer over Inv_OccuranceTime lat/lng with district-to-station drill-down | Hotspot map interactive with filters |
| 6 | Explainable risk score | Repeat-offender score per PersonEntity with feature-importance breakdown | Score card shows contributing factors |
| 7 | Anomaly detection | Manufactured hotspot week (3x spike) triggers alert | Alert marker visible on dashboard |
| 8 | "Ask Berunda" RAG | 3 rehearsed questions return grounded, cited answers | Answers show source citations |
| 9 | Auth + RBAC | 3 roles (Investigator, SCRB, Compliance) see different views | Role-switching demo |
| 10 | Audit logging | Person-level read and AI-output view produce AuditLog entries | Audit log queryable |
| 11 | Fairness check | CasteID/ReligionID confirmed absent from model features and role-restricted | Fairness dashboard shows green check |
| 12 | Demo evidence pack | Recorded walkthrough, README, architecture docs | Submission ready |

## 11-Day Release Plan

### Day 1-2: Foundation

**Person A (Data/Backend):**
- Create Catalyst project, set up Data Store schema (source tables + Berunda extensions)
- Write synthetic data generator (Faker en_IN): 2000-5000 FIRs with planted patterns
- Plant: 1 repeat-offender across 4 cases, 1 shared-vehicle across 3 cases, 1 hotspot week

**Person B (AI/Frontend):**
- Scaffold React frontend on Catalyst Slate
- Build shell navigation (Investigator Console / Hotspot Map / Network Graph / Ask Berunda)
- Set up Catalyst Authentication with 3 demo roles

### Day 3-4: Entity Resolution & NLP

**Person A:**
- Build English NER pipeline (spaCy) as Catalyst Function
- Build entity resolution matcher: blocking (same district/age-band) + weighted similarity
- Test against planted "same person, 4 cases" record

**Person B:**
- Build Investigator Console case list + detail view against real data
- Wire "linked persons" panel to PersonEntityLink

### Day 5-6: Risk Scoring, Hotspots, Anomalies

**Person A:**
- Configure QuickML AutoML on PersonEntity features (HARD EXCLUDE CasteID/ReligionID)
- Build anomaly z-score check (district, crime_type, week)

**Person B:**
- Build hotspot map (hexbin over lat/lng), district-to-station drill-down
- Wire risk score + feature-importance into person-detail view

### Day 7-8: Graph and Polish

**Person A:**
- Build graph traversal over RelationshipEdge (degree, shortest path)
- Confirm shared-vehicle link surfaces correctly

**Person B:**
- Build Network/Link-Analysis Graph dashboard (force-directed layout)
- Polish SCRB State Command View

### Day 9: RAG and Fairness

**Both:**
- Set up QuickML RAG + LLM serving over curated case summaries
- Build 3-5 rehearsed demo questions
- Build Fairness Auditor: check CasteID/ReligionID exclusion + role restriction

### Day 10: Integration

**Both:**
- Wire Catalyst Auth + API Gateway in front of all routes
- Confirm audit logging fires on every sensitive read
- Full end-to-end run-through (no new features)

### Day 11: Demo and Submission

**Both:**
- Write demo script, record walkthrough
- Final pass on documentation and submission artifacts

## Scope Protection Rules

1. New feature requests after Day 8 are automatically deferred to STRETCH or VISION
2. If any MVP feature is at risk of not completing by Day 9, implement the smallest credible version (fallback) rather than cutting entirely
3. Demo quality trumps feature count — polish 10 working features over shipping 12 broken ones
4. Days 10-11 are frozen for integration, testing, and demo prep — no new code
