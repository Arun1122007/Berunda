# Project Berunda — Implementation Plan
## Companion document 3 of 5 — Karnataka State Police Datathon 2026

Task-level build plan for a 2-person team, 11 days. This is the "what do I actually open my laptop and do" document — the Complete Roadmap covers the strategic phases, this covers the daily checklist.

---

## Day 0 — Before You Start Coding

- [ ] Create the Catalyst project (both team members added as collaborators)
- [ ] Set up GitHub repo, `main`/`dev` branch split, connect Catalyst Pipelines for CI/CD
- [ ] Confirm your exact submission format on the Hack2Skill dashboard (video? live link? repo? deck?) — do this first, it changes what "done" means on Day 11
- [ ] Agree the team split: **Person A = Data/Backend** (schema, agents 8.1-8.8, DevOps), **Person B = AI/Frontend** (agents 8.9-8.13, dashboards)
- [ ] Both read the Database & ER Reference doc (companion doc 5) before writing any migration code

---

## Day 1-2 — Foundation

**Person A:**
- [ ] Migrate the real schema (CaseMaster, Accused, Victim, ComplainantDetails, ArrestSurrender, Act/Section, lookup tables) into Catalyst Data Store
- [ ] Add the Berunda-extension tables: `PersonEntity`, `PersonEntityLink`, `RelationshipEdge`, `RiskScore`, `MoPattern`, `MoTag`, `Vehicle`, `VehicleLink`, `AuditLog`
- [ ] Write the synthetic data generator (Python + Faker `en_IN` / indic-faker):
  - Target: ~2,000-5,000 synthetic FIRs, ~800 synthetic accused persons, ~1,200 synthetic victims
  - **Deliberately plant:** one person appearing as accused in 4 different `CaseMasterID`s under 4 different names/ages (to prove entity resolution works), one vehicle linked across 3 cases, one 2-week window with a 3x spike in one crime type in one district (to prove anomaly detection works)
  - Seed the RNG so the demo is reproducible

**Person B:**
- [ ] Scaffold the frontend project on Catalyst Slate/Web Client Hosting
- [ ] Build the shell navigation (Investigator Console / Hotspot Map / Network Graph / Ask Berunda — even with placeholder data)
- [ ] Set up Catalyst Authentication with 2-3 demo roles (Investigator, SCRB, Compliance-Reporting)

**Checkpoint (end of Day 2):** synthetic data loaded, both can query it, frontend shell deployed and reachable.

---

## Day 3-4 — Entity Resolution & NLP (the load-bearing piece)

**Person A:**
- [ ] Build the English NER pipeline (spaCy) as a Catalyst Function — extract person names, ages, addresses from `Inv_OccuranceTime.BriefFacts`
- [ ] Build the entity-resolution matcher: blocking (same district/age-band) + weighted similarity scoring (name similarity + address overlap) → writes to `PersonEntity`/`PersonEntityLink`
- [ ] **Test specifically against your planted "same person, 4 different cases" synthetic record** — this is your proof-of-concept checkpoint, don't move on until this works
- [ ] Stretch (if ahead of schedule): swap in an AI4Bharat Kannada NER model for a bilingual demo

**Person B:**
- [ ] Build the Investigator Console's case list + case detail view against real (synthetic) data
- [ ] Wire the "linked persons" panel to `PersonEntityLink` output from Person A

**Checkpoint (end of Day 4):** typing/loading a FIR narrative resolves to the correct existing `PersonEntity` if that person has prior cases.

---

## Day 5-6 — Risk Scoring, Hotspots, Anomalies

**Person A:**
- [ ] Configure Zia AutoML on `PersonEntity`-aggregated features (prior case count, offense-type diversity, recency) — **explicitly exclude `CasteID`/`ReligionID` and any address-as-identity-proxy field from the training set**
- [ ] Pull the feature-importance output QuickML/Zia generates natively — wire it into the `RiskScore.feature_importance` field
- [ ] Build the anomaly z-score check: rolling (district, crime_type, week) counts vs. historical baseline

**Person B:**
- [ ] Build the hotspot map (hexbin/heatmap over `Inv_OccuranceTime.latitude/longitude`), district → station drill-down
- [ ] Wire the risk score + feature-importance breakdown into the Investigator Console's person-detail view

**Checkpoint (end of Day 6):** a risk score is visible with a human-readable "why" breakdown; the manufactured hotspot week is visible on the map.

---

## Day 7-8 — Link Analysis Graph & Dashboard Polish

**Person A:**
- [ ] Build graph traversal over `RelationshipEdge` (degree, shortest path) — surface "this person connects to N other open cases"
- [ ] Confirm the planted shared-vehicle link across 3 cases surfaces correctly

**Person B:**
- [ ] Build the Network/Link-Analysis Graph dashboard (force-directed layout, e.g. vis-network or D3)
- [ ] Polish the SCRB State Command View (KPI tiles, trend lines)

**Checkpoint (end of Day 8):** clicking a suspect in the console shows their full graph of connections, visually.

---

## Day 9 — Ask Berunda & Fairness Check

**Both:**
- [ ] Set up Catalyst QuickML's RAG + LLM serving over a small curated set of case summaries
- [ ] Build 3-5 rehearsed demo questions that reliably return good grounded answers (don't rely on live improvisation for the judged demo)
- [ ] Build the Fairness Auditor's basic check: confirm programmatically that `CasteID`/`ReligionID` never appear in any `RiskScore.feature_importance` payload, and that the general dashboard roles cannot query those two columns at all
- [ ] Run this fairness check live as part of the demo — this is a differentiator almost no other team will show

---

## Day 10 — Integration, Auth, Audit

**Both:**
- [ ] Wire Catalyst Authentication + API Gateway in front of every Function/dashboard route
- [ ] Confirm audit logging fires on every person-level record read and every AI-recommendation view
- [ ] Full end-to-end run-through, twice, with fresh browser sessions (catch anything that only works because of leftover local state)
- [ ] Fix whatever breaks — do not add new features today

---

## Day 11 — Demo & Submission

- [ ] Write the demo script (see companion doc `Project_Berunda_Hackathon_Pitch.md` for the recommended narrative order)
- [ ] Record the demo video / rehearse the live walkthrough at least twice
- [ ] Final pass on whichever submission artifact is required (repo README, deck, or both)
- [ ] Submit with time to spare — don't use the deadline itself as a buffer

---

## Pre-Submission Checklist

- [ ] Every ✅ BUILDABLE feature from the Blueprint actually works live, not just in code
- [ ] Every 🔭 VISION feature is clearly labeled as roadmap in the pitch materials — don't let a judge catch you overclaiming
- [ ] The `CasteID`/`ReligionID` governance behavior is demonstrable, not just described
- [ ] The entity-resolution "same person, different case IDs" proof is demonstrable, not just described
- [ ] Team names, project name (Berunda), and Catalyst service usage are consistent across the repo, deck, and demo
