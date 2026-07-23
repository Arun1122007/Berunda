# Project Berunda
## An AI-Native Crime Intelligence Operating System for Karnataka State Police

**Submission for:** Datathon 2026 — "AI-Driven Crime Analytics & Visualization Platform" (Hack2Skill × Karnataka State Police)
**Team:** Phoenix Coder (2 members)
**Document type:** Full enterprise blueprint + hackathon-executable core (Phase 1 sections are marked ✅ BUILDABLE; forward-looking sections are marked 🔭 VISION)
**Mandatory deployment target:** Catalyst by Zoho

---

> **A note on how to read this document.** You asked for the maximal, no-detail-spared version — so that's what follows. But a 2-person team has ~11 days until submission closes, not 11 months. Every section below is tagged so you always know what to actually *build* versus what to *write and present as roadmap*:
> - ✅ **BUILDABLE** — realistic for 2 people in the time you have; this is your demo.
> - 🧩 **STRETCH** — doable if Phase 1 goes fast; nice-to-have for the live demo.
> - 🔭 **VISION** — real, detailed, defensible design — but documented, not built, for this submission. This is what makes the doc read like an enterprise blueprint instead of a hackathon README.
>
> Judges score on innovation, impact, technical depth, scalability, and presentation — a small working system backed by a document like this outperforms either a toy demo with no depth, or 40 pages of prose with nothing running behind it.

---

## Table of Contents

1. Executive Summary
2. Market & Competitive Research
3. Stakeholders
4. Requirements
5. Enterprise Architecture
6. Data Architecture & Database Design
7. AI Architecture
8. Agent Ecosystem
9. Signature AI Features
10. Data Science Methodology
11. Visualization & Dashboards
12. Security Architecture
13. Governance, Ethics & Bias Mitigation
14. DevOps & Deployment
15. Catalyst by Zoho — Mandatory Service Mapping
16. Implementation Roadmap
17. Open Source & Reference Stack
18. Ten-Year Vision
19. Appendix: Naming, Research Notes & References

---

## 1. Executive Summary

### 1.1 Mission
Give the Karnataka State Police (KSP) and the State Crime Records Bureau (SCRB) one living, queryable picture of crime across the state — replacing the current reality of fragmented Excel sheets with a system that connects every FIR, person, location, and case to every other one, in real time, in both Kannada and English.

### 1.2 Vision
Project Berunda is named after the *Gandaberunda* — the two-headed mythical bird that is Karnataka's own state emblem, printed on every KSRTC bus and government letterhead in the state. The two heads are the design metaphor for the platform itself: one head watches backward across 30 years of historical case data to find hidden connections; the other watches forward, forecasting where and when the next incident is statistically likely, so patrols can be proactive instead of reactive.

### 1.3 The Problem, Precisely
- **Data silos.** Crime data lives in independent station-level Excel sheets and legacy CCTNS entries that don't talk to each other.
- **No relationship intelligence.** A suspect involved in five incidents across three districts currently looks like five unrelated case files, because nothing cross-references people, vehicles, and locations across cases.
- **Reactive posture.** Without pattern discovery, patrol deployment and resource allocation happen after crime spikes, not before.
- **SCRB blindness.** The state bureau receives whatever fragments individual stations choose to report, not a live, structured feed.

### 1.4 Why Existing Systems Don't Solve This
| System | What it does well | Where it falls short for KSP's stated problem |
|---|---|---|
| **CCTNS** (national) | Standardized FIR digitization, national interoperability | Built for record-keeping and inter-state lookup, not analytics, link-analysis, or prediction — it is a system of record, not a system of intelligence |
| **NCRB / ICJS** | National crime statistics, judiciary-police-prison data exchange | Aggregate, retrospective reporting cadence (annual/quarterly), not a live investigator-facing tool |
| **Palantir Gotham** | Best-in-class entity resolution and link analysis at scale | Proprietary, extremely expensive, closed-source, not deployable under an open-source/Catalyst-mandatory constraint |
| **IBM i2 Analyst's Notebook** | Mature link-chart analysis, used by many law enforcement agencies globally | Desktop-centric, license-per-seat, no native AI/ML or geospatial prediction layer, no open API for a modern cloud-native stack |
| **PredPol**-style predictive policing tools | Hotspot forecasting | Widely criticized for feedback-loop bias (over-policing already over-policed areas) with no published bias-mitigation methodology |

**Berunda's positioning:** it does not try to replace CCTNS — it sits on top of it as an intelligence layer, ingesting CCTNS/station data and adding the three things none of the above provide together in one open, Catalyst-native package: (1) cross-case relationship graphs, (2) explainable predictive risk scoring with built-in bias auditing, and (3) bilingual (Kannada + English) natural-language investigation support.

### 1.5 Expected Impact
- **Investigators:** minutes instead of days to see every prior incident connected to a suspect, vehicle, or location.
- **SCRB:** a live, drillable state map instead of a quarterly PDF.
- **Citizens:** faster case resolution via better-targeted patrol deployment, and a governance model designed from day one to avoid profiling by identity markers.
- **Government:** an open-core system Karnataka can own and extend, instead of a recurring-license dependency on a closed foreign platform.

---

## 2. Market & Competitive Research

### 2.1 Detailed Comparison Matrix

| Capability | CCTNS | NCRB/ICJS | Palantir Gotham | IBM i2 | PredPol-style | **Project Berunda** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| FIR digitization & national lookup | ✅ | ✅ | — | — | — | Ingests from CCTNS |
| Cross-case link analysis / network graphs | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| Predictive hotspot forecasting | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ (with bias audit) |
| Repeat-offender risk scoring | ❌ | ❌ | ✅ | ❌ | Partial | ✅ (explainable) |
| Bilingual regional-language NLP (Kannada) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Open source / state-owned | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Real-time interactive dashboards | ❌ | ❌ | ✅ | Partial | Partial | ✅ |
| Built-in fairness/bias governance | ❌ | ❌ | Undisclosed | ❌ | Widely criticized | ✅ (by design) |
| Cost model | Govt-funded | Govt-funded | Enterprise license (high) | Per-seat license | SaaS license | Open-core on Catalyst |

### 2.2 What "Superior" Actually Means Here
Berunda doesn't out-engineer Palantir on raw capability — no 2-person hackathon team could claim that credibly, and a judge who knows the space would immediately discount an overclaim. Berunda's real edge is **fit**: it is the only option in the table that is simultaneously (a) open-source and state-owned, (b) natively bilingual for Karnataka, and (c) designed with bias auditing as a first-class citizen rather than a bolt-on — three things none of the closed enterprise platforms prioritize because they weren't built for an Indian state police context.

---

## 3. Stakeholders

| Stakeholder | Primary need from Berunda |
|---|---|
| Investigating Officers (IOs) | Fast cross-referencing of suspects/vehicles/locations across cases |
| Station House Officers (SHOs) | Local dashboard: what's happening in my jurisdiction right now |
| SCRB | State-wide drillable analytics, trend alerts, statutory reporting |
| Superintendents of Police (district-level) | Resource deployment recommendations, hotspot maps |
| Cyber Crime Cells | OSINT and digital-evidence correlation tooling |
| Forensic Labs | Evidence metadata linkage, chain-of-custody tracking |
| Judiciary / Courts | Structured case timelines (read-only, access-controlled) |
| Home Ministry / DGP Office | State-level KPI dashboards |
| Women Safety Wing | Crime-against-women pattern and hotspot views |
| Traffic Police | Vehicle-linked incident cross-referencing |
| Citizens (indirect) | Faster resolution, transparent governance safeguards |
| NGOs / Researchers (restricted, anonymized access) | Aggregate trend data for policy research |

---

## 4. Requirements

### 4.1 Functional Requirements (excerpt — full list in Section 8/9 per module)
- FR1: Ingest FIR/incident records (structured import + manual entry) in English and Kannada.
- FR2: Automatically extract entities (persons, locations, vehicles, weapons, organizations) from free-text FIR narrative.
- FR3: Maintain a relationship graph connecting persons↔incidents↔locations↔vehicles with confidence scores.
- FR4: Compute an explainable repeat-offender risk score per person, with feature-importance breakdown.
- FR5: Render spatiotemporal hotspot maps with drill-down from state → district → station jurisdiction.
- FR6: Detect anomalous spikes in a crime category vs. historical baseline and alert SCRB.
- FR7: Provide natural-language query over the case corpus ("show me all robbery cases linked to this vehicle") via RAG.
- FR8: Maintain immutable audit logs for every AI-assisted decision surfaced to an officer.
- FR9: Role-based dashboards per stakeholder type (Section 3).

### 4.2 Non-Functional Requirements
| Category | Requirement |
|---|---|
| Scalability | Architecture must not structurally block scaling to 10M+ records / 30 years of history (Phase 1 demo can run on a sample dataset) |
| Availability | 99.5%+ target at state-deployment maturity (not a Phase-1 concern) |
| Security | Encryption at rest and in transit; RBAC; audit logging on all sensitive reads |
| Compliance | DPDP Act 2023 / DPDP Rules 2025 alignment (Section 13.4) |
| Accessibility | Kannada + English UI and NLP from day one |
| Explainability | No "black box" score may reach an officer's screen without a feature-importance breakdown |
| Human-in-the-loop | The system never auto-triggers action; it only informs. All watchlist/patrol decisions remain human-made and logged |

### 4.3 Assumption Flag
This document assumes a generic crime-record schema (FIR / Incident / Person / Location / Vehicle / Evidence) modeled on standard Indian FIR structure, since the specific ER diagram linked in your Resources tab wasn't available to reference directly. **Section 6's schema should be reconciled against that actual dataset before you build against it** — if you share it, the schema and sample queries can be tightened to match exactly.

---

## 5. Enterprise Architecture

### 5.1 Architectural Style
Berunda uses a **modular microservices** approach on top of **event-driven** communication, deliberately kept simpler than full CQRS/event-sourcing for Phase 1 (that complexity is real, but premature for a 2-person team — it's documented here as the Phase 3+ evolution, not the MVP).

- ✅ BUILDABLE (Phase 1): Functions-based microservices, direct REST calls, a single Data Store schema, synchronous ingestion.
- 🔭 VISION (Phase 3+): Full event-driven mesh with Catalyst Signals, CQRS read/write separation for the analytics layer, event sourcing for full audit replay.

### 5.2 High-Level System Diagram

```mermaid
flowchart TB
    subgraph Ingestion["Ingestion Layer"]
        A1[CCTNS / Station Excel Import]
        A2[FIR Manual Entry Form]
        A3[OSINT / Public Feed Connectors]
    end

    subgraph Storage["Catalyst Storage Layer"]
        B1[(Catalyst Data Store - relational)]
        B2[(Catalyst NoSQL - unstructured notes/media metadata)]
        B3[(Catalyst Stratus - evidence files/images)]
        B4[(Catalyst Cache)]
    end

    subgraph Processing["Processing & AI Layer"]
        C1[Catalyst Functions - business logic]
        C2[Catalyst QuickML - NER, risk scoring, RAG]
        C3[Catalyst Zia Services - OCR, image/object recognition]
        C4[Agent Orchestration - Section 8]
    end

    subgraph Access["Access & Delivery Layer"]
        D1[Catalyst API Gateway]
        D2[Catalyst Authentication]
        D3[Catalyst Slate / Web Client Hosting]
    end

    subgraph UX["Dashboards"]
        E1[Investigator Console]
        E2[SCRB State Command View]
        E3[Geospatial Hotspot Map]
        E4[Network / Link-Analysis Graph]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B2
    B1 --> C1
    B2 --> C1
    B3 --> C3
    C1 --> C2
    C2 --> C4
    C3 --> C4
    C4 --> D1
    B1 --> B4
    D1 --> D2
    D1 --> D3
    D3 --> E1
    D3 --> E2
    D3 --> E3
    D3 --> E4
```

### 5.3 Design Decisions & Trade-offs

| Decision | Chosen approach | Alternative considered | Why chosen |
|---|---|---|---|
| Backend compute | Catalyst Functions for stateless logic, AppSail for the always-on API layer | Full Kubernetes microservices | Catalyst deployment is mandatory for this submission; Functions/AppSail cover the same architectural role at far lower operational overhead for a 2-person team |
| Primary data store | Catalyst Data Store (relational, SQL) | Pure NoSQL / document store | Crime records are highly relational (person-incident-location); relational integrity matters more than write-throughput at this stage |
| Unstructured notes/media metadata | Catalyst NoSQL | Force everything into SQL | Beat notes, OSINT captures, and free-text vary in shape; forcing a rigid schema on them early would slow ingestion |
| Graph/network layer | Computed in-application over relational join tables for Phase 1; dedicated graph DB (Neo4j) as Phase 3 upgrade | Standing up a graph DB immediately | A join-table model is enough to demo relationship discovery at hackathon scale; a real graph DB earns its complexity only once record volume is large |
| LLM / RAG | Catalyst QuickML's built-in LLM serving (Qwen models) + RAG over the knowledge base | Self-hosted open-weight LLM | Mandatory-Catalyst constraint, plus QuickML already ships this natively - no reason to rebuild it |
| API layer | Catalyst API Gateway in front of Functions | Custom Express/FastAPI gateway | Gateway is a listed mandatory-mapping capability (#18); using it directly also gets you throttling/auth for free |

---

## 6. Data Architecture & Database Design

> Reminder of the assumption flagged in 4.3: the schema below is a defensible, standard-FIR-structure design. Swap in the real fields from your Resources-tab ER diagram before you build.

### 6.1 Core Entity-Relationship Diagram

```mermaid
erDiagram
    PERSON ||--o{ PERSON_INCIDENT_LINK : involved_in
    INCIDENT ||--o{ PERSON_INCIDENT_LINK : has
    INCIDENT }o--|| LOCATION : occurred_at
    INCIDENT ||--o{ EVIDENCE : has
    PERSON ||--o{ RELATIONSHIP : source_of
    PERSON ||--o{ RELATIONSHIP : target_of
    INCIDENT ||--o{ VEHICLE_INCIDENT_LINK : involves
    VEHICLE ||--o{ VEHICLE_INCIDENT_LINK : linked_to
    PERSON ||--o{ RISK_SCORE : scored
    INCIDENT ||--o{ MO_TAG : tagged_with
    MO_PATTERN ||--o{ MO_TAG : classifies

    PERSON {
        string person_id PK
        string full_name
        string aliases
        date dob
        string gender
        string id_proof_type
        string id_proof_number_encrypted
        string category
        string photo_ref
    }
    INCIDENT {
        string incident_id PK
        string fir_number
        string crime_type
        string ipc_bns_sections
        datetime reported_at
        string location_id FK
        string station_id
        text description_kannada
        text description_english
        string status
    }
    LOCATION {
        string location_id PK
        float latitude
        float longitude
        string district
        string taluk
        string police_station_id
    }
    PERSON_INCIDENT_LINK {
        string link_id PK
        string person_id FK
        string incident_id FK
        string role
        float confidence_score
    }
    RELATIONSHIP {
        string relationship_id PK
        string person_id_a FK
        string person_id_b FK
        string relationship_type
        string source_incident_id FK
        float confidence_score
    }
    VEHICLE {
        string vehicle_id PK
        string plate_number
        string vehicle_type
        string owner_person_id FK
    }
    VEHICLE_INCIDENT_LINK {
        string link_id PK
        string vehicle_id FK
        string incident_id FK
        float confidence_score
    }
    EVIDENCE {
        string evidence_id PK
        string incident_id FK
        string evidence_type
        string storage_ref
        string custody_hash
    }
    RISK_SCORE {
        string score_id PK
        string person_id FK
        string score_type
        float value
        datetime computed_at
        string model_version
        json feature_importance
    }
    MO_PATTERN {
        string mo_id PK
        text description
        json embedding_vector_ref
    }
    MO_TAG {
        string tag_id PK
        string incident_id FK
        string mo_id FK
        float match_confidence
    }
    AUDIT_LOG {
        string log_id PK
        string actor_id
        string action
        string entity_type
        string entity_id
        datetime timestamp
        text justification
    }
```

### 6.2 Storage Tiering Strategy

| Data type | Store | Retention / archival note |
|---|---|---|
| Structured FIR/incident/person/location records | Catalyst Data Store | Active for 7 years hot, archived to Stratus cold-tier beyond (30-year historical requirement is a Phase 4+/state-deployment concern, not Phase 1) |
| Free-text notes, OSINT captures, beat diaries | Catalyst NoSQL | Indexed for full-text search |
| Evidence files (images, scans, audio) | Catalyst Stratus (S3-style object storage) | Immutable once written; custody hash logged in EVIDENCE.custody_hash |
| Frequently-hit lookups (station lists, jurisdiction boundaries) | Catalyst Cache | TTL-based invalidation |
| Every AI-assisted decision surfaced to a human | AUDIT_LOG table, append-only | Never deleted; this is your compliance backbone (see Section 13) |

### 6.3 Indexing & Query Notes
- Composite index on (district, crime_type, reported_at) for the hotspot dashboard's most common filter pattern.
- Full-text index on description_kannada and description_english for the NLP/RAG layer.
- RELATIONSHIP and PERSON_INCIDENT_LINK are the two tables that do the heavy lifting for link-analysis - index both foreign keys, and keep confidence_score indexed since the dashboard will routinely filter out low-confidence auto-extracted links.

---

## 7. AI Architecture

### 7.1 Design Philosophy
Berunda is **AI-assisted, not AI-automated**. Every model output that reaches a human is a *recommendation with a visible reason*, never an autonomous action. This isn't just an ethical stance — it's also the more defensible engineering choice for a government submission, since "the AI decides" is both a harder sell to judges and a real accountability risk in a policing context.

### 7.2 Layers

```mermaid
flowchart LR
    subgraph L1["Layer 1: Perception"]
        P1[Kannada+English NER]
        P2[OCR - Zia Services]
        P3[Entity Resolution]
    end
    subgraph L2["Layer 2: Reasoning"]
        R1[Risk Scoring - QuickML AutoML]
        R2[Link/Graph Analysis]
        R3[Hotspot Forecasting]
        R4[Anomaly Detection]
    end
    subgraph L3["Layer 3: Synthesis"]
        S1[RAG-based Case Q&A]
        S2[Auto-drafted Case Summaries]
    end
    subgraph L4["Layer 4: Governance"]
        G1[Bias/Fairness Audit Agent]
        G2[Explainability Layer]
        G3[Audit Logging]
    end
    L1 --> L2 --> L3
    L2 --> L4
    L3 --> L4
```

- **Perception layer** turns raw text/images into structured entities. ✅ BUILDABLE (Phase 1): English NER via spaCy-style pipeline deployed as a Catalyst Function; Kannada NER as 🧩 STRETCH using an AI4Bharat/IndicNLP model if time allows, otherwise documented as Phase 2.
- **Reasoning layer** is where the actual predictive/analytical value lives — risk scores, hotspot clusters, anomaly flags, link discovery. ✅ BUILDABLE for a reduced feature set on sample data; 🔭 VISION at full 10M-record, 30-year scale.
- **Synthesis layer** is the natural-language interface — "ask the case corpus a question in plain English or Kannada, get a cited answer." ✅ BUILDABLE as a thin RAG demo over a small document set using Catalyst QuickML's LLM serving + RAG.
- **Governance layer** is not optional and not last — it runs alongside every other layer, logging and checking outputs. ✅ BUILDABLE as a lightweight rule-based fairness check in Phase 1 (Section 13.2); 🔭 VISION as a full learned bias-detection model at scale.

### 7.3 Why Not "100 Agents" for Real
Document 2's brief calls for 100+ specialized agents. At true enterprise/national scale that's a legitimate target-state architecture — but naming 100 agents in a hackathon doc without being able to explain any of them in depth reads as padding to an experienced judge, not ambition. Section 8 below specifies **13 real agents in full depth** — enough to cover FIR intake, link analysis, prediction, dashboards, and governance end-to-end — plus the extensibility pattern that lets the same framework scale toward the full agent mesh described in Document 2 (documented in 7.4).

### 7.4 Agent Extensibility Pattern (how you get from 13 to 100+ later)
Every agent in Berunda follows one contract: `input schema -> tool calls -> model call -> output schema + confidence + audit entry`. Because every agent obeys the same contract and registers itself with the same orchestrator, adding a new specialized agent (e.g., a future Drone-Feed Agent or Dark-Web Monitoring Agent) is a matter of implementing that contract, not redesigning the system. This is the actual mechanism — not just a claim — by which the platform scales from 13 agents at hackathon stage to a full agent ecosystem at national deployment.

---

## 8. Agent Ecosystem

Each agent below is specified with Purpose, Inputs, Outputs, Tools, Underlying model, and a feasibility tag.

### 8.1 FIR Intake & Bilingual NLP Agent
- **Purpose:** Convert raw FIR text (Kannada or English) into structured entities.
- **Inputs:** Free-text FIR narrative, station metadata.
- **Outputs:** Extracted persons, locations, vehicles, weapons, organizations with confidence scores; writes to `PERSON_INCIDENT_LINK`, `VEHICLE_INCIDENT_LINK`.
- **Tools:** spaCy/AI4Bharat NER models, Catalyst Zia keyword extraction.
- **Model:** Fine-tuned multilingual NER (English fully supported Phase 1; Kannada 🧩 STRETCH).
- **Decision flow:** text -> language detect -> NER -> entity resolution against existing `PERSON`/`VEHICLE` records -> confidence-scored link write.
- **Feasibility:** ✅ BUILDABLE (English), 🧩 STRETCH (Kannada).

### 8.2 Case Triage & Prioritization Agent
- **Purpose:** Rank incoming cases by urgency/severity for SHO attention.
- **Inputs:** Crime type, location risk score, historical resolution time for similar cases.
- **Outputs:** Priority score + one-line justification.
- **Tools:** Rule-based scoring (Phase 1) -> QuickML classification model (Phase 2).
- **Feasibility:** ✅ BUILDABLE.

### 8.3 Link Analysis / Network Agent
- **Purpose:** Build and query the person-incident-location-vehicle relationship graph; surface "this suspect connects to 4 other open cases."
- **Inputs:** `RELATIONSHIP`, `PERSON_INCIDENT_LINK`, `VEHICLE_INCIDENT_LINK` tables.
- **Outputs:** Graph traversal results for the Link-Analysis dashboard (Section 11).
- **Tools:** In-application graph traversal (Phase 1, join-table based) -> Neo4j/NetworkX community-detection (Phase 3).
- **Model:** Non-ML graph algorithms (degree centrality, shortest path) Phase 1; graph embeddings Phase 3.
- **Feasibility:** ✅ BUILDABLE (core traversal), 🔭 VISION (embeddings/community detection at scale).

### 8.4 MO (Modus Operandi) Pattern-Matching Agent
- **Purpose:** Flag incidents that share a modus operandi with prior cases, even across districts.
- **Inputs:** `description_english`/`description_kannada`, crime type, method-of-entry/approach fields.
- **Outputs:** `MO_TAG` entries with match confidence.
- **Tools:** Text embedding similarity (sentence-transformers) over `MO_PATTERN.embedding_vector_ref`.
- **Feasibility:** 🧩 STRETCH — a simplified keyword/embedding-similarity version is buildable; full trajectory-level MO clustering is 🔭 VISION.

### 8.5 Repeat-Offender Risk Scoring Agent
- **Purpose:** Produce an explainable risk score per known offender, based on offense history and recency — never on identity markers.
- **Inputs:** Prior incident count, recency, offense-type diversity, resolution outcomes.
- **Outputs:** `RISK_SCORE` row with `feature_importance` JSON.
- **Tools:** Catalyst QuickML AutoML (classification/regression) — feature importance and model explanation are native QuickML features.
- **Hard constraint (non-negotiable):** caste, religion, community, and other identity/proxy variables are explicitly excluded from the feature set, and this exclusion is documented and testable (Section 13.2).
- **Feasibility:** ✅ BUILDABLE on sample data.

### 8.6 Spatiotemporal Hotspot Agent
- **Purpose:** Cluster incidents by time + location to surface emerging hotspots.
- **Inputs:** `LOCATION`, `reported_at`, `crime_type`.
- **Outputs:** Hotspot polygons/heatmap layers for the geospatial dashboard.
- **Tools:** Simple density clustering (Phase 1: grid/hexbin aggregation, e.g. the same approach Kepler.gl's hexbin layer uses) -> DBSCAN/spatio-temporal clustering (Phase 2+).
- **Feasibility:** ✅ BUILDABLE.

### 8.7 Anomaly Detection Agent
- **Purpose:** Alert when a crime category spikes vs. its historical baseline in a region.
- **Inputs:** Rolling counts per (district, crime_type, week).
- **Outputs:** Alert record + magnitude of deviation.
- **Tools:** Simple statistical z-score/rolling-average deviation (Phase 1) -> QuickML anomaly/forecasting model (Phase 2).
- **Feasibility:** ✅ BUILDABLE.

### 8.8 Evidence & Chain-of-Custody Agent
- **Purpose:** Track evidence handoffs and flag custody gaps.
- **Inputs:** Evidence upload events, custody transfer logs.
- **Outputs:** Custody hash chain, gap alerts.
- **Tools:** Hash chaining stored in `EVIDENCE.custody_hash`; Catalyst Stratus for the underlying files.
- **Feasibility:** 🧩 STRETCH (basic hash-chain demo is buildable; full blockchain-anchored version is 🔭 VISION, see 12.4).

### 8.9 Case Summary / Investigation Assistant Agent ("Ask Berunda")
- **Purpose:** Natural-language Q&A over the case corpus — "summarize all open cases linked to vehicle KA-05-XXXX."
- **Inputs:** User query (English or Kannada), retrieved case documents.
- **Outputs:** Cited, grounded natural-language answer.
- **Tools:** Catalyst QuickML LLM serving (Qwen 2.5-14B-Instruct) + RAG over the case knowledge base — both features QuickML ships natively.
- **Feasibility:** ✅ BUILDABLE as a scoped demo (small document set, English-first).

### 8.10 OSINT / Public-Source Monitoring Agent
- **Purpose:** Pull relevant public-source signals (news, public social posts about local incidents) into the intelligence picture.
- **Inputs:** Public web/news feeds.
- **Outputs:** Candidate leads for human review only — never auto-added to a person's profile.
- **Tools:** Scheduled scraping (Catalyst Cron/Job Scheduling) + entity matching against existing records.
- **Feasibility:** 🔭 VISION for this submission (real OSINT ingestion raises data-provenance and privacy questions that deserve more than hackathon-timeline treatment — documented honestly rather than faked for the demo).

### 8.11 Cross-Case / Serial-Incident Correlation Agent
- **Purpose:** Surface multi-case links a human might miss (e.g., same MO + adjacent geography + overlapping time window across three "unrelated" open cases).
- **Inputs:** Outputs of 8.3, 8.4, 8.6.
- **Outputs:** "These 3 cases may be connected" suggestion with supporting evidence links, for human review.
- **Feasibility:** 🧩 STRETCH — buildable as a rules-based combination of the other agents' outputs; full serial-crime-detection ML is 🔭 VISION.

### 8.12 Natural-Language Dashboard Query Agent
- **Purpose:** Let a non-technical officer type/speak a question and get a chart or map back.
- **Inputs:** Natural-language query.
- **Outputs:** Generated query against the Data Store + rendered chart/map.
- **Tools:** QuickML LLM serving translating intent -> parameterized query template (not free-form SQL generation, to avoid injection risk).
- **Feasibility:** 🧩 STRETCH.

### 8.13 Governance & Bias-Audit Agent
- **Purpose:** Continuously check that risk-scoring outputs don't correlate with excluded identity variables or their proxies (e.g., surname patterns, neighborhood-as-proxy-for-community), and that every AI-assisted decision surfaced to a human has a logged justification.
- **Inputs:** Model feature sets, `RISK_SCORE` distributions, `AUDIT_LOG`.
- **Outputs:** Fairness report, flagged proxy-variable warnings.
- **Tools:** Statistical parity checks (Phase 1, simple); learned fairness auditing (Phase 3+).
- **Feasibility:** ✅ BUILDABLE as a real, if simple, check — and this is one of your strongest differentiators to actually demo, because almost no competing team will bother.

---

## 9. Signature AI Features

These are the "beyond the brief" ideas — each one is tagged for feasibility so the doc stays honest about what's demoed live vs. designed on paper.

| Feature | What it does | Feasibility |
|---|---|---|
| **Bilingual FIR Understanding** | Reads Kannada or English FIR narrative and extracts structured entities either way | ✅ BUILDABLE (English) / 🧩 STRETCH (Kannada) |
| **Explainable Repeat-Offender Score** | Every risk score ships with a feature-importance breakdown an officer can actually read | ✅ BUILDABLE |
| **"Ask Berunda" Investigation Assistant** | Plain-language Q&A over the case corpus, grounded and cited, in Kannada or English | ✅ BUILDABLE (English demo) |
| **Hidden-Link Discovery** | Surfaces a suspect/vehicle/location connection across cases that looks unrelated in isolated records | ✅ BUILDABLE |
| **Crime Hotspot Pulse Map** | District -> station drill-down heatmap with time-of-day layering | ✅ BUILDABLE |
| **Fairness Auditor** | Ongoing check that risk scores don't proxy for identity variables | ✅ BUILDABLE |
| **MO Fingerprinting** | Groups incidents by shared method, even across districts | 🧩 STRETCH |
| **Serial-Incident Correlator** | Flags "these 3 open cases might be one actor" | 🧩 STRETCH |
| **Living Case Timeline** | Auto-reconstructed chronological view of a case from all linked records | 🧩 STRETCH |
| **Cross-State Correlation** | Matching MO/entities against other states' CCTNS data | 🔭 VISION — requires inter-state data-sharing agreements, a policy dependency, not just an engineering one |
| **Autonomous Draft Intelligence Reports** | Auto-drafted (human-reviewed, never auto-sent) weekly SCRB briefing | 🔭 VISION |
| **Crime Simulation Sandbox** | "What if resource X moved to district Y" scenario modeling | 🔭 VISION |
| **Living Criminal Digital Twin** | Full behavioral profile across time — this is powerful and also the single feature most likely to raise real profiling/privacy concerns if built without very strict governance; documented deliberately as 🔭 VISION with a governance-first design note, not built |

**Honest note on the more speculative items:** several ideas in the original brief (digital twin, autonomous report generation, cross-state correlation) are genuinely interesting but carry real privacy and due-process implications if implemented naively. Presenting them as researched, governance-aware roadmap items — rather than claiming they're built — is both more credible to a judging panel and the responsible way to handle them.

---

## 10. Data Science Methodology

### 10.1 Model Selection by Task

| Task | Phase 1 approach | Scaled approach |
|---|---|---|
| Repeat-offender risk scoring | Logistic regression / gradient-boosted trees via Catalyst QuickML AutoML | XGBoost/LightGBM with hyperparameter search, monitored drift |
| Hotspot forecasting | Grid/hexbin aggregation + rolling averages | Spatio-temporal clustering (DBSCAN variants), Bayesian spatial models |
| Anomaly detection | Z-score deviation from rolling baseline | Isolation Forest / seasonal-decomposition-based anomaly models |
| MO similarity | Sentence-embedding cosine similarity | Fine-tuned domain embedding model + graph neural network over the MO co-occurrence graph |
| NER (entity extraction) | spaCy pipeline (English), AI4Bharat model (Kannada) | Fine-tuned transformer NER on Karnataka-specific FIR corpus |
| Case Q&A | RAG over small curated set via QuickML LLM serving | Full knowledge-graph-augmented RAG (GraphRAG) over the complete case corpus |

### 10.2 Evaluation & Monitoring
- Every model ships with a **feature-importance report** (native to QuickML) reviewed before deployment.
- **Fairness metrics** (demographic parity proxy-check, Section 13.2) computed alongside standard accuracy/F1/precision-recall — a model that scores well on accuracy but fails the fairness check does not ship.
- **Drift monitoring:** scheduled (Catalyst Cron) re-evaluation against a held-out recent window; alert if performance or fairness metrics degrade beyond threshold.
- **Retraining cadence:** quarterly at pilot scale, or triggered by drift-alert.

---

## 11. Visualization & Dashboards

### 11.1 Dashboard Inventory

| Dashboard | Primary user | Core visual elements |
|---|---|---|
| Investigator Console | IO / SHO | Case list, linked-entity panel, "Ask Berunda" query box |
| Geospatial Hotspot Map | SCRB, district SP | District -> station drill-down heatmap, time-of-day slider, red-pulse alert markers for spikes |
| Network / Link-Analysis Graph | IO, cyber cell | Node-link graph: persons/vehicles/locations, edge thickness = confidence |
| State Command View | SCRB, DGP office | KPI tiles, trend lines, cross-district comparison |
| Fairness & Audit Dashboard | Governance officer | Score-distribution-by-group parity charts, audit log search |

### 11.2 Implementation Notes
- Geospatial layer: hexbin/heatmap rendering pattern modeled on **Kepler.gl** (MIT-licensed, built for exactly this kind of large-scale geospatial visualization) — can be embedded directly or reimplemented lightweight inside the Catalyst-hosted web client.
- Network graph: force-directed layout (D3.js or a lightweight vis-network component).
- All dashboards served via Catalyst Slate / Web Client Hosting, behind Catalyst Authentication + API Gateway.
- UI text and NLP query box support both Kannada and English labels from Phase 1, even where backend Kannada NLP is still 🧩 STRETCH — the interface commitment to bilingual support should be visible even before every backend model is.

---

## 12. Security Architecture

### 12.1 Identity & Access
- **Authentication:** Catalyst Authentication (built-in) for all users; MFA required for any account with access to person-level (not aggregate) records.
- **Authorization:** RBAC as the Phase 1 baseline (Investigator / SHO / SCRB / Admin / Governance-Auditor roles), with a documented path to ABAC (attribute-based, e.g. "district-scoped access only") as the Phase 3 upgrade for state-wide deployment.
- **Zero Trust framing:** every service-to-service call is authenticated (no implicit trust from network position), even internally between Catalyst Functions — practically enforced via the API Gateway sitting in front of all Functions rather than allowing direct function-to-function calls that bypass auth.

### 12.2 Data Protection
- Encryption at rest (Catalyst Data Store/Stratus native encryption) and in transit (TLS everywhere, enforced at the API Gateway and Domain Mappings layer).
- Sensitive fields (`id_proof_number`, precise home address of victims/witnesses) stored encrypted at the column level, not just at the storage-volume level.
- Secrets (API keys, model credentials) never hardcoded — stored via Catalyst's secrets management, rotated on a defined schedule.

### 12.3 Audit & Immutable Logging
- Every read of a person-level record by an investigator, and every AI-assisted recommendation surfaced to a human, writes an `AUDIT_LOG` row: who, what, when, why.
- `AUDIT_LOG` is append-only at the application layer for Phase 1; a hash-chained (tamper-evident) version is the Phase 3 target — this is the same pattern as evidence chain-of-custody (8.8) and can share the same hashing utility.

### 12.4 Evidence Integrity
- ✅ BUILDABLE: SHA-256 hash chain over evidence custody events, stored in `EVIDENCE.custody_hash`, verifiable on demand.
- 🔭 VISION: anchoring that hash chain to a permissioned blockchain ledger for cross-agency tamper-evidence — genuinely useful at state scale, genuinely overkill to build for a demo, and honestly presented as such rather than name-dropped without substance.

### 12.5 Standards Alignment
- **OWASP Top 10** — input validation, injection prevention (parameterized queries only; the NL-to-query agent in 8.12 explicitly avoids free-form SQL generation for this reason), secure session handling.
- **ISO 27001 / NIST** — referenced as the target control framework for the state-deployment phase; Phase 1 implements the practical subset relevant to a web app handling sensitive personal data (access control, encryption, logging, incident response plan).
- **DPDP Act 2023 / DPDP Rules 2025** — see Section 13.4 for the specific, current legal framing.

---

## 13. Governance, Ethics & Bias Mitigation

### 13.1 Why This Section Is Not Decorative
Predictive policing tools have a well-documented failure mode: they learn from historical enforcement patterns, which can themselves reflect uneven policing intensity across neighborhoods — and then the tool recommends more enforcement in the same places, reinforcing the original pattern. A credible submission has to name this risk directly and show a concrete mitigation, not just an "Ethics ✅" checkbox.

### 13.2 Concrete Bias Mitigation Design
- **Feature exclusion list (hard constraint):** caste, religion, community name, and any field that acts as a strong proxy for them (e.g., surname alone, specific micro-neighborhood as a standalone feature) are excluded from every predictive model's feature set. This is enforced in code (a checked allow-list of permitted features per model), not just written policy.
- **Parity monitoring:** the Governance & Bias-Audit Agent (8.13) computes score-distribution comparisons across recorded demographic groups where legally captured, on a read-only basis, purely to detect disparate model behavior — never as a model input.
- **Human-in-the-loop, always:** no score or flag from Berunda ever triggers an automatic action (no auto-adding to a watchlist, no auto-dispatch). Every use is advisory, and every use is logged with the acting officer's justification.
- **Right to explanation:** any officer using a risk score can see the feature-importance breakdown behind it, in the dashboard itself, not buried in a technical report.

### 13.3 AI Governance Structure (target-state, documented as 🔭 VISION for process, ✅ BUILDABLE for the technical hooks)
- **Model Registry:** every deployed model version, its training data window, and its fairness-check results logged.
- **Human review board:** before any new predictive model moves from pilot to production, a review board (SCRB + legal + an independent ethics reviewer) signs off — this is a process commitment, documented here as the intended operating model rather than something a hackathon submission can itself demonstrate.
- **Versioning & rollback:** any model version can be rolled back to the prior version if a fairness or accuracy regression is detected post-deployment.

### 13.4 Legal Compliance — DPDP Act 2023
India's data protection law is the Digital Personal Data Protection Act, 2023, which became operationally concrete once the DPDP Rules 2025 were notified in November 2025, with compliance obligations phasing in over roughly the following year and a half. Section 17 of the Act allows the Central Government to exempt specified government instrumentalities from most of the Act's provisions when processing is necessary for sovereignty, security, or public order — a provision directly relevant to a state police intelligence platform. Berunda's design choice is to build as if the stricter, non-exempted obligations apply anyway (purpose limitation, storage limitation, security safeguards, breach notification) — both because that's the more defensible long-term position for public trust, and because it's the harder, more credible engineering story to tell a judging panel.

---

## 14. DevOps & Deployment

### 14.1 Pipeline
- **CI/CD:** Catalyst Pipelines for build/test/deploy automation, triggered on every commit to the main branch.
- **Infrastructure as Code:** Catalyst's project-config-as-code (catalyst-config) checked into version control alongside application code — the Catalyst-native equivalent of a Terraform-style IaC approach, since standing up a separate Terraform layer would be redundant with Catalyst's own project provisioning.
- **Environments:** separate Catalyst projects for Dev / Staging / Production, promoted through Pipelines.

### 14.2 Observability
- ✅ BUILDABLE: Catalyst's built-in Functions logs and API Gateway request metrics, reviewed manually during the hackathon window.
- 🔭 VISION: Prometheus/Grafana-style dashboards and OpenTelemetry tracing once the system runs on always-on AppSail services at pilot scale — genuinely valuable at that stage, not necessary to fake for a demo.

### 14.3 Deployment Strategy
- Phase 1: single-environment direct deploy via Catalyst Pipelines.
- Phase 3+: blue-green or canary rollout for model updates specifically (since a bad model version is the highest-risk deployment type in this system, given Section 13's governance commitments) — documented as the intended pattern, not built now.

---

## 15. Catalyst by Zoho — Mandatory Service Mapping

Full mapping against the required capability table from your Resources tab, plus per-module rationale, alternatives, and scaling notes.

| # | Capability | Catalyst Service | Berunda module using it | Why this service | Future-enterprise alternative | Scaling note |
|---|---|---|---|---|---|---|
| 1 | Serverless functions/backend logic | Catalyst Serverless (Functions) | All agent logic (Section 8), business rules | Mandatory; matches the stateless-agent contract in 7.4 | Kubernetes microservices | Functions scale automatically per-invocation; revisit only past very high sustained throughput |
| 2 | Docker image deployment | Catalyst AppSail (custom OCI runtime) | Any custom ML runtime not natively supported by QuickML (e.g. a custom Kannada NER container) | Needed if a Phase 2 Kannada model requires a custom runtime | Self-managed container host | Fine as-is through state-deployment scale |
| 3 | Full web app in managed runtime | Catalyst AppSail (managed runtime) | Always-on API layer for the dashboard backend | Needed for persistent connections the pure-Functions model doesn't fit well | Traditional VM-hosted app server | Vertical scale first, then horizontal |
| 4 | Frontend / SPA / static site | Catalyst Slate / Web Client Hosting | All dashboards (Section 11) | Mandatory hosting target | Vercel/Netlify-style host | CDN-backed, scales natively |
| 5 | Custom domain + SSL | Catalyst Domain Mappings | Public-facing SCRB/investigator portal | Mandatory | Cloudflare/manual cert management | No change needed at scale |
| 6 | Relational database | Catalyst Data Store | Core schema (Section 6) | Crime records are highly relational | Managed PostgreSQL | Partition by district/year at national scale |
| 7 | Unstructured/semi-structured data | Catalyst NoSQL | Beat notes, OSINT captures, free-text metadata | Schema flexibility for irregular field-collected data | MongoDB Atlas | Shard by station/date at scale |
| 8 | Object/blob storage | Catalyst Stratus | Evidence files, scanned FIRs, photos | Mandatory S3-style store | AWS S3/MinIO | Lifecycle policies for cold-tier archival |
| 9 | Cache | Catalyst Cache | Jurisdiction lookups, session data | Reduces repeated Data Store hits on hot paths | Redis | Straightforward horizontal scale |
| 10 | Full-text search | Catalyst Data Store (native full-text) | FIR narrative search | Native capability, no extra service | Elasticsearch | Elasticsearch becomes worth the operational cost past a few million documents |
| 11 | Text LLMs / RAG / knowledge bases | Catalyst QuickML (LLM Serving, RAG) | Ask Berunda (8.9), NL dashboard query (8.12) | Mandatory; ships Qwen-model serving + RAG natively | Self-hosted open-weight LLM | Scale via QuickML's managed serving tier |
| 12 | No-code ML pipelines | Catalyst QuickML | Risk scoring, anomaly detection pipeline setup | Mandatory; avoids hand-rolling ML infra | Kubeflow/MLflow pipeline | Sufficient through pilot scale |
| 13 | Automated model training (tabular) | Catalyst Zia AutoML | Repeat-offender risk model (8.5) | Mandatory; native AutoML with feature importance | XGBoost/LightGBM custom training | Custom training justified only once feature engineering outgrows AutoML's defaults |
| 14 | OCR / Face / Text / Image / Barcode / ID | Catalyst Zia Services | Scanned FIR OCR, evidence photo tagging | Mandatory | Google Vision API | Sufficient at all demonstrated scales |
| 15 | Voice/speech services | Catalyst Zia Services | 🔭 VISION: voice FIR intake in Kannada | Mandatory when built | AI4Bharat speech models self-hosted | Deferred to Phase 2+ |
| 16 | PDF/report generation, headless browser | Catalyst SmartBrowz | Auto-generated case summary PDFs, SCRB weekly report exports | Mandatory | Puppeteer self-hosted | Sufficient at all scales |
| 17 | User auth / login | Catalyst Authentication | All role-based access (Section 12.1) | Mandatory | Auth0/Okta | Add SSO/SAML at state-deployment scale |
| 18 | API routing/throttling/auth | Catalyst API Gateway | Front door for all Functions/dashboards | Mandatory; also your Zero Trust enforcement point (12.1) | Kong/Apigee | Add rate-limit tiers per stakeholder class at scale |
| 19 | OAuth tokens for 3rd-party services | Catalyst Connections | Future CCTNS API bridge, OSINT feed auth | Needed once real CCTNS integration is pursued | Manual token management | N/A |
| 20 | Scheduled jobs/cron | Catalyst Cron / Job Scheduling | Anomaly baseline recompute, drift-check, OSINT polling | Mandatory | Airflow | Sufficient through pilot scale |
| 21 | Reacting to in-project events | Catalyst Signals + Event Functions | 🔭 VISION: real-time alert-on-insert pipeline | Needed for the full event-driven Phase 3 architecture (5.1) | Kafka + custom consumers | Deferred past Phase 1 |
| 22 | Cross-app event bus | Catalyst Signals | 🔭 VISION: multi-district event routing at state scale | Same as above | Kafka | Deferred |
| 23 | Multi-step workflow orchestration | Catalyst Circuits | 🔭 VISION: multi-agent orchestration with branching (7.4 at scale) | Phase 1 orchestration is simple direct calls; Circuits earns its complexity once the agent count grows | Temporal/Airflow | Deferred |
| 24 | Transactional email | Catalyst Mail | Alert notifications to SHOs/SCRB | Mandatory | SendGrid | Sufficient at all scales |
| 25 | Push notifications | Catalyst Push Notifications | 🧩 STRETCH: mobile hotspot-alert push | Mandatory when built | Firebase Cloud Messaging | Sufficient at all scales |
| 26 | CI/CD | Catalyst Pipelines | Section 14.1 | Mandatory | GitHub Actions + Terraform | Sufficient at all scales |

---

## 16. Implementation Roadmap

### 16.1 Phase 1 — MVP (your actual 11-day build, 2 people)
**Goal: a working, demoable slice that touches every layer of the architecture, not a mockup.**

| Day range | Work |
|---|---|
| Day 1-2 | Catalyst project setup; Data Store schema (Section 6) migrated; sample dataset loaded (real or synthetic if the real KSP dataset can't be shared publicly) |
| Day 3-4 | FIR intake + English NER (8.1) as a Catalyst Function; entity resolution against `PERSON`/`VEHICLE` |
| Day 5-6 | Risk scoring (8.5) via Zia AutoML; hotspot aggregation (8.6); anomaly z-score check (8.7) |
| Day 7-8 | Link-analysis graph traversal (8.3) + dashboard front-end (Investigator Console, Hotspot Map, Network Graph) on Slate/Web Client Hosting |
| Day 9 | "Ask Berunda" RAG demo (8.9) over a small curated case set; Fairness Auditor (8.13) basic parity check |
| Day 10 | Auth (Catalyst Authentication) wired in, API Gateway in front of everything, audit logging live |
| Day 11 | Demo script, recording/deck, final documentation pass |

**Two-person split suggestion:** one person owns Data/Backend (Sections 6, 8.1-8.8, 14), the other owns AI/Frontend (Sections 8.9-8.13, 11) — with a shared checkpoint at Day 6 and Day 9 to integrate.

### 16.2 Phase 2 — Pilot (post-hackathon, if selected)
Kannada NLP, MO fingerprinting, serial-incident correlator, push notifications, real CCTNS data-bridge pilot with one district.

### 16.3 Phase 3 — District Deployment
Event-driven architecture (Signals/Circuits), graph database migration (Neo4j), ABAC access control, blockchain-anchored evidence chain, full observability stack.

### 16.4 Phase 4 — State Deployment
Full 30-year historical data ingestion and archival tiering, state-wide SCRB command view, OSINT monitoring agent (with legal review completed), full governance board process live.

### 16.5 Phase 5 — National Rollout
Cross-state correlation (contingent on inter-state data-sharing agreements), NCRB/ICJS deep integration, national crime knowledge graph.

### 16.6 Phase 6 — International Adaptation
Localization framework for other states'/countries' languages and legal frameworks, generalized crime-ontology layer decoupled from India-specific FIR structure.

**Risks & dependencies across phases:** data-sharing MOUs (Phase 4-5), legal review for OSINT/voice ingestion (Phase 2-4), sustained state IT budget for AppSail/observability scale-up (Phase 3+), and — the risk worth naming explicitly — sustained governance-board bandwidth, since the fairness commitments in Section 13 only mean something if the human review process is actually staffed and followed at scale.

---

## 17. Open Source & Reference Stack

| Tool | License | Role in Berunda |
|---|---|---|
| **OpenAleph** (OCCRP) + **FollowTheMoney** schema | MIT / Open source | Reference model for the entity/relationship ontology in Section 6 — don't reinvent this, adapt it |
| **Kepler.gl** | MIT | Reference implementation pattern for the geospatial hotspot/heatmap dashboard (Section 11) |
| **Neo4j Community Edition** / **NetworkX** | GPL/community + BSD | Phase 3 graph-database upgrade path for link analysis (8.3) |
| **spaCy** | MIT | English NER pipeline (8.1) |
| **AI4Bharat / IndicNLP** models | Various open licenses | Kannada NLP (8.1, Phase 2 Kannada support) |
| **sentence-transformers** | Apache 2.0 | MO similarity embeddings (8.4) |
| **scikit-learn / XGBoost / LightGBM** | BSD/Apache | Reference models behind the scenes of Zia AutoML choices, useful for offline experimentation before committing to a QuickML config |

**Open-core strategy for the project itself:** publish the core schema, agent contracts (7.4), and non-sensitive dashboard components as an open GitHub repo under Apache 2.0, with a `CONTRIBUTING.md`, issue templates, and a plugin pattern for new agents — matching Document 2's "open core" ask, scoped so it's genuinely maintainable by a small team rather than promising a full community governance model you can't yet staff.

---

## 18. Ten-Year Vision (🔭 VISION — presented as researched roadmap, not commitment)

- **Edge AI on body-worn/patrol-vehicle cameras** for real-time, on-device object/plate recognition, feeding back only structured events (not raw video) to preserve privacy-by-design.
- **Drone-feed integration** for large-event crowd/incident monitoring, with the same governance-first framing as OSINT (8.10) — human-reviewed, never autonomous.
- **Smart-city sensor fusion** (traffic cameras, IoT) as additional, clearly-labeled-confidence input signals to the hotspot model, not silent ground truth.
- **National Crime Knowledge Graph**, federated across states with each state retaining data sovereignty — technically and politically the hardest item on this list, flagged honestly as such.
- **Responsible-AI maturity model**: a public, versioned record of every fairness audit result, so the governance commitments in Section 13 remain a living practice, not a one-time hackathon claim.

---

## 19. Appendix: Naming, Research Notes & References

### 19.1 Why "Project Berunda"
Named for the *Gandaberunda* — the two-headed mythical bird that is the official emblem of the Government of Karnataka, visible on KSRTC buses and state letterhead across the state. It is not a generic Sanskrit buzzword; it is *specifically* Karnataka's own symbol, which makes it both distinctive and locally resonant to the judging panel. The two heads map directly onto the platform's dual posture: one head reviewing history (link analysis, MO patterns), the other watching forward (hotspot/risk prediction).

### 19.2 Names checked and rejected (with reasons)
| Name | Status | Reason |
|---|---|---|
| Trinetra | ❌ Rejected | Already in live use: UP Police's "Trinetra 2.0" app with a CrimeGPT module, and separately Akola Police's unrelated "Project Trinetra" for predictive policing |
| Kavach | ❌ Rejected | Already in live use: NIC's government "Kavach Authentication" app, and the Shark-Tank-funded "AI Kavach" fraud-protection product |
| Vajra / Rakshak | ❌ Rejected | Common, already-used Indian security/govt branding terms |
| NetrAstra | ✅ Clean (backup option) | No collisions found; more generic/pan-India-sounding if you want a non-Karnataka-specific alternative |
| **Berunda** | ✅ Clean (recommended) | No tech/software collisions; uniquely tied to Karnataka's own state identity |

### 19.3 Key External References Consulted
- CCTNS / NCRB / ICJS — existing Indian government crime-record systems, used as the comparison baseline in Section 2.
- OCCRP OpenAleph and the FollowTheMoney data schema — open source investigative-data platform used as the reference model for the entity/relationship design in Section 6.
- Kepler.gl (Uber / OpenJS Foundation) — open source geospatial visualization library referenced for the hotspot dashboard pattern in Section 11.
- Zoho Catalyst QuickML documentation — confirmed native LLM serving, RAG, and AutoML with feature-importance capabilities referenced throughout Sections 7-8 and 15.
- India's Digital Personal Data Protection Act, 2023 and DPDP Rules 2025 — referenced for the compliance framing in Section 13.4.
- Publicly reported critiques of predictive-policing systems (e.g. PredPol-style feedback-loop bias) — referenced in Section 13.1 as the reason the governance layer isn't decorative.

### 19.4 What to double-check before you build
1. **The actual ER diagram / dataset** from your Resources tab — Section 6's schema is a reasonable default, not a guaranteed match. Reconcile before writing migration scripts.
2. **Exact submission format** (video demo? live deploy link? GitHub repo? slide deck?) — check your Submissions/Interactions dashboard tabs directly, since that's behind your login and wasn't visible to cross-reference here.
3. **Judging rubric specifics for this exact datathon**, if published anywhere on your dashboard beyond what's generically true of Hack2Skill events — weight your Day 10-11 polish time accordingly.

---

*End of document. Project Berunda — Team Phoenix Coder — Datathon 2026.*
