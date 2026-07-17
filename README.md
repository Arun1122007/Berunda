# Project Berunda

**AI-Native Crime Intelligence Platform for Karnataka State Police**

[//]: # (Document ID: BERUNDA-README | Status: DRAFT | Classification: PUBLIC)

---

## One-Line Value Proposition

Berunda transforms fragmented FIR records into a connected, queryable intelligence layer — geospatial hotspots, criminal link networks, and a grounded natural-language investigation assistant, built entirely on the mandatory Zoho Catalyst stack.

## Problem & Solution

**Problem:** Karnataka's SCRB manages crime data in station-level Excel silos with no systematic link analysis, no proactive tooling, and fragmented visibility across districts.

**Solution:** A single platform where raw FIR data is ingested and normalized; analysts see spatiotemporal hotspots with temporal patterns; investigators see relationship graphs linking persons, locations, and vehicles across cases; and anyone can ask questions in plain English for grounded, cited answers.

## MVP Capabilities (BUILDABLE)

1. Synthetic FIR import and entity extraction (English)
2. Cross-case person entity resolution with confidence scoring
3. Case/person relationship graph and hidden-link discovery
4. Geospatial hotspot map with district-to-station drill-down
5. Explainable risk scoring with feature-importance breakdown
6. Anomaly and spike detection against historical baselines
7. "Ask Berunda" grounded RAG over curated case corpus
8. Role-based authentication and authorization
9. Audit logging for sensitive reads and AI-assisted outputs
10. Live sensitive-feature exclusion and fairness verification

## Architecture Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React + Tailwind, MapLibre GL (maps), Cytoscape.js (graphs) |
| API & Logic | Catalyst Serverless Functions + API Gateway |
| ML Serving | Catalyst AppSail (Python: NetworkX, scikit-learn) |
| AI/LLM | Catalyst QuickML (LLM Serving, RAG, AutoML) |
| Relational Data | Catalyst Data Store |
| Unstructured Data | Catalyst NoSQL |
| File Storage | Catalyst Stratus |
| Auth | Catalyst Authentication |
| Automation | Catalyst Cron |

Full architecture documentation: `docs/04_ARCHITECTURE/`

## Responsible-Use Boundary

- **AI outputs are advisory only.** No score or flag triggers automatic enforcement action.
- **Every AI-assisted decision is logged** with officer justification.
- **Caste and religion fields are hard-excluded** from all predictive models and role-restricted to statutory compliance reporting only.
- **No individual criminality prediction.** Risk scoring is based on offense history and recency, never on identity markers.

## Synthetic-Data Notice

All person-level data in the demo is synthetically generated using Faker (`en_IN` locale) and indic-faker. No real victim, accused, or witness data is used. Every synthetic record is clearly labeled.

## Documentation Navigation

| Section | Contents |
|---------|----------|
| `docs/00_START_HERE.md` | Entry point and reading guide |
| `docs/01_DISCOVERY/` | Source inventory, contradictions, gap register |
| `docs/02_STRATEGY_AND_PRODUCT/` | Charter, PRD, personas, use cases |
| `docs/03_REQUIREMENTS/` | SRS, NFRs, traceability matrix |
| `docs/04_ARCHITECTURE/` | HLD, LLD, ADRs, Catalyst mapping |
| `docs/05_DATA/` | ERD reconciliation, data model, synthetic data spec |
| `docs/06_AI_AND_ANALYTICS/` | AI/ML spec, RAG spec, model cards |
| `docs/08_SECURITY_PRIVACY_GOVERNANCE/` | Threat model, PIA, AI impact assessment |
| `docs/11_DELIVERY/` | Implementation plan, backlog, risk register, demo plan |

## Live vs Roadmap Distinction

| Status | Meaning |
|--------|---------|
| ✅ BUILDABLE | Implemented in the MVP demo |
| 🧩 STRETCH | Buildable if time allows |
| 🔭 VISION | Documented as roadmap, not built |

---

*For the full project baseline, start at `docs/00_START_HERE.md`.*
