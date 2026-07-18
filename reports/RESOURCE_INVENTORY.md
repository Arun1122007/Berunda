# Resource Inventory

> **Document ID:** BERUNDA-REP-INVENTORY-001 | **Version:** 1.0 | **Status:** INITIAL
> **Classification:** INTERNAL | **Owner:** Berunda Team | **Source:** Blueprint §C + expansion
> **Generated:** 2026-07-18T04:30:00Z | **Last Verified:** 2026-07-18

---

## 1. Summary

### 1.1 By Status

| Status | Count | Definition |
|--------|-------|------------|
| present-and-verified | 0 | Downloaded, checksummed, quality gates passed |
| missing | 92 | Not yet acquired — queued for download |
| inaccessible | 8 | Behind login/auth wall (RSRC-001–008) |
| not-required | 12 | P4 / FUTURE-RESTRICTED — deliberately excluded |
| **Total** | **112** | |

### 1.2 By Priority

| Priority | Count | Description |
|----------|-------|-------------|
| P0 — Competition-critical | 8 | RSRC-001–008 |
| P1 — Prototype-critical | 25 | RSRC-009–033 |
| P2 — Enterprise-enrichment | 30 | RSRC-034–063 |
| P3 — Future authorized integrations | 17 | RSRC-064–080 |
| P4 — Research-only | 12 | RSRC-081–092 |
| **Total** | **92** | |

### 1.3 By Category (D1–D14)

| Category | Count | Resource IDs |
|----------|-------|--------------|
| D1 — Official Datathon Material | 8 | RSRC-001–008 |
| D2 — Zoho Catalyst Platform | 7 | RSRC-009–015 |
| D3 — Crime & Public-Safety Statistics | 10 | RSRC-016–025 |
| D4 — Administrative & Geospatial Data | 10 | RSRC-026–035 |
| D5 — Census, Socio-Economic Indicators | 10 | RSRC-036–045 |
| D6 — Weather, Environment, Temporal | 10 | RSRC-046–055 |
| D7 — Legal & Classification References | 10 | RSRC-056–065 |
| D8 — Ontologies, Schemas, Interoperability | 5 | RSRC-066–070 |
| D9 — Similar Systems & Open-Source Repos | 10 | RSRC-071–080 |
| D10 — Research Papers, Benchmarks | 5 | RSRC-081–085 |
| D11 — Frontend, Visualization | 5 | RSRC-086–090 |
| D12/D13 — Backend, Synthetic Data | 2 | RSRC-091–092 |
| D14 — Security, Privacy, Governance | 5 | RSRC-093–097 |
| D15 — Infrastructure & DevOps | 5 | RSRC-098–102 |
| *Overflow / unassigned* | *0* | *RSRC-103–112 reserved* |

---

## 2. P0 — Competition-Critical (RSRC-001–008)

| RSRC ID | Blueprint Ref | Resource | Priority | Status | Notes |
|---------|---------------|----------|----------|--------|-------|
| RSRC-001 | R001 | Datathon ERD / DB Design Document | P0 | inaccessible | Behind organizer login — in hand as PDF |
| RSRC-002 | R001 | Police FIR Schema — table definitions | P0 | inaccessible | Behind organizer login |
| RSRC-003 | R002 | Challenge rules, timeline, judging criteria | P0 | inaccessible | Login-gated at `hack2skill.com` |
| RSRC-004 | R002 | Submission format requirements | P0 | inaccessible | Login-gated — must confirm before Day 10 |
| RSRC-005 | R002 | FAQ / support resources | P0 | inaccessible | Login-gated |
| RSRC-006 | R003 | Catalyst credit redemption code KSPH26 | P0 | inaccessible | Console-gated at `catalyst.zoho.com` |
| RSRC-007 | R003 | Catalyst project provisioning guide | P0 | inaccessible | Console-gated |
| RSRC-008 | — | Datathon sample data (if provided separately) | P0 | missing | Not yet confirmed by organizers |

## 3. P1 — Prototype-Critical (RSRC-009–033)

| RSRC ID | Blueprint Ref | Resource | Priority | Status | Notes |
|---------|---------------|----------|----------|--------|-------|
| RSRC-009 | R004 | Zoho Catalyst — Data Store documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-010 | R004 | Zoho Catalyst — Functions documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-011 | R004 | Zoho Catalyst — AppSail documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-012 | R004 | Zoho Catalyst — Authentication docs | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-013 | R005 | Catalyst QuickML — LLM serving docs | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-014 | R005 | Catalyst QuickML — RAG quickstart | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-015 | R005 | Catalyst QuickML — AutoML / feature importance | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-016 | R006 | NCRB — Crime in India 2022 (full volume) | P1 | missing | `ncrb.gov.in` |
| RSRC-017 | R006 | NCRB — Crime in India 2021 (full volume) | P1 | missing | `ncrb.gov.in` |
| RSRC-018 | R007 | NCRB on OGD Platform — CSV datasets | P2 | missing | `data.gov.in` |
| RSRC-019 | R008 | KSP — Monthly Crime Review (latest) | P1 | missing | `ksp.karnataka.gov.in` |
| RSRC-020 | R008 | KSP — Monthly Crime Review (previous year) | P2 | missing | `ksp.karnataka.gov.in` |
| RSRC-021 | R009 | NITI NDAP — Crime in India: IPC Statistics | P2 | missing | `ndap.niti.gov.in` |
| RSRC-022 | R011 | OpenStreetMap — Karnataka POIs (Overpass) | P1 | missing | `overpass-api.de` |
| RSRC-023 | R012 | Bhuvan — WMS terrain layers (Karnataka) | P1 | missing | `bhuvan.nrsc.gov.in` |
| RSRC-024 | R012 | Bhuvan — satellite imagery layers | P2 | missing | `bhuvan.nrsc.gov.in` |
| RSRC-025 | R013 | Survey of India — admin boundaries | P2 | missing | License unverified |
| RSRC-026 | R014 | Census 2011 — District Census Handbook (Karnataka) | P2 | missing | `censusindia.gov.in` |
| RSRC-027 | R014 | Census 2011 — Population tables (Karnataka) | P2 | missing | `censusindia.gov.in` |
| RSRC-028 | R015 | NITI NDAP — socio-economic indicators (general) | P2 | missing | `ndap.niti.gov.in` |
| RSRC-029 | R017 | Open-Meteo — historical weather (Karnataka) | P1 | missing | `open-meteo.com` |
| RSRC-030 | R018 | IMD — gridded rainfall data (Karnataka) | P2 | missing | Access method unconfirmed |
| RSRC-031 | R019 | ECI — Karnataka election dates / schedule | P2 | missing | `eci.gov.in` |
| RSRC-032 | R020 | BNS 2023 — full Act text | P0 | missing | `indiacode.nic.in` |
| RSRC-033 | R021 | BNSS 2023 — full Act text | P1 | missing | `indiacode.nic.in` |

## 4. P2 — Enterprise-Enrichment (RSRC-034–063)

| RSRC ID | Blueprint Ref | Resource | Priority | Status | Notes |
|---------|---------------|----------|----------|--------|-------|
| RSRC-034 | R022 | DPDP Act 2023 — full text | P1 | missing | `indiacode.nic.in` |
| RSRC-035 | R022 | DPDP Rules 2025 — full text | P1 | missing | `indiacode.nic.in` |
| RSRC-036 | R023 | BPRD — BNS Practitioner Handbook | P4 | not-required | Guidance only |
| RSRC-037 | R024 | GeoJSON specification (RFC 7946) | P4 | not-required | Open standard |
| RSRC-038 | R024 | OGC WMS/WFS standards | P4 | not-required | Open standard |
| RSRC-039 | R025 | POLE data-model reference papers | P4 | not-required | Design pattern |
| RSRC-040 | R026 | OpenAleph / FollowTheMoney schema | P1 | missing | `github.com` — reference |
| RSRC-041 | R027 | Kepler.gl — reference implementation | P1 | missing | `github.com` |
| RSRC-042 | R028 | Neo4j Community Edition installer | P2 | missing | `neo4j.com` — Phase 3 |
| RSRC-043 | R029 | NetworkX — graph library | P2 | missing | `pip install networkx` |
| RSRC-044 | R030 | MapLibre GL JS — map rendering | P2 | missing | `npm install maplibre-gl` |
| RSRC-045 | R031 | Cytoscape.js — graph rendering | P2 | missing | `npm install cytoscape` |
| RSRC-046 | R032 | Faker (`en_IN` locale) — synthetic data | P1 | missing | `pip install Faker` |
| RSRC-047 | R033 | indic-faker — Kannada synthetic text | P2 | missing | Source unverified |
| RSRC-048 | R034 | OWASP ASVS — Application Security Standard | P4 | not-required | Reference only |
| RSRC-049 | R034 | OWASP API Security Top 10 | P4 | not-required | Reference only |
| RSRC-050 | R035 | NIST CSF — Cybersecurity Framework | P4 | not-required | Reference only |
| RSRC-051 | R035 | NIST AI RMF — AI Risk Management | P4 | not-required | Reference only |
| RSRC-052 | — | Catalyst — Cron trigger documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-053 | — | Catalyst — API Gateway documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-054 | — | Catalyst — Stratus documentation | P1 | missing | `help.catalyst.zoho.com` |
| RSRC-055 | — | Catalyst — SmartBrowz documentation | P2 | missing | `help.catalyst.zoho.com` |
| RSRC-056 | — | Catalyst — Catalyst CLI / ZCCTL documentation | P2 | missing | `help.catalyst.zoho.com` |
| RSRC-057 | — | NCRB — Crime in India 2020 | P2 | missing | Historical baseline |
| RSRC-058 | — | NCRB — Crime in India 2019 | P2 | missing | Historical baseline |
| RSRC-059 | — | Census 2011 — literacy data (Karnataka) | P2 | missing | `censusindia.gov.in` |
| RSRC-060 | — | Census 2011 — urban-rural breakdown | P2 | missing | `censusindia.gov.in` |
| RSRC-061 | — | NITI NDAP — education indicators | P2 | missing | `ndap.niti.gov.in` |
| RSRC-062 | — | NITI NDAP — health indicators | P2 | missing | `ndap.niti.gov.in` |
| RSRC-063 | — | NITI NDAP — infrastructure indicators | P2 | missing | `ndap.niti.gov.in` |

## 5. P3 — Future Authorized Integrations (RSRC-064–080)

| RSRC ID | Blueprint Ref | Resource | Priority | Status | Notes |
|---------|---------------|----------|----------|--------|-------|
| RSRC-064 | — | CCTNS — live incident feed interface contract | P3 | not-required | FUTURE-RESTRICTED — MOU required |
| RSRC-065 | — | CCTNS — FIR schema (production) | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-066 | — | CCTNS — accused/victim records (real) | P3 | not-required | FUTURE-RESTRICTED — PII |
| RSRC-067 | — | Telecom CDR — lawful intercept interface | P3 | not-required | FUTURE-RESTRICTED — warrant required |
| RSRC-068 | — | Banking / UPI transaction records | P3 | not-required | FUTURE-RESTRICTED — court order |
| RSRC-069 | — | Aadhaar / UIDAI authentication | P3 | not-required | FUTURE-RESTRICTED — legal review |
| RSRC-070 | — | ICAO / Passport records | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-071 | — | State-wide accused database (cross-district) | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-072 | — | Witness protection program records | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-073 | — | Forensic lab reports (FSL) live feed | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-074 | — | Prison / jail management system records | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-075 | — | Court case management system (e-Courts) | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-076 | — | Traffic challan / e-challan database | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-077 | — | Vehicle registration (RTO / VAHAN) | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-078 | — | Driver license records (SARATHI) | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-079 | — | Armed Forces / paramilitary deployment data | P3 | not-required | FUTURE-RESTRICTED |
| RSRC-080 | — | Intelligence Bureau (IB) / state intelligence inputs | P3 | not-required | FUTURE-RESTRICTED |

## 6. P4 — Research-Only (RSRC-081–092)

| RSRC ID | Blueprint Ref | Resource | Priority | Status | Notes |
|---------|---------------|----------|----------|--------|-------|
| RSRC-081 | D10 | Predictive policing — critique literature | P4 | not-required | Research-inform, not integrate |
| RSRC-082 | D10 | Entity resolution / record linkage benchmarks | P4 | not-required | Inform entity design |
| RSRC-083 | D10 | Kernel density estimation for hotspot detection | P4 | not-required | Algorithm reference |
| RSRC-084 | D10 | Explainability methods for risk scoring (SHAP/LIME) | P4 | not-required | Algorithm reference |
| RSRC-085 | D10 | DBSCAN and spatial clustering benchmarks | P4 | not-required | Algorithm reference |
| RSRC-086 | — | Catalyst — DevOps / CI/CD documentation | P4 | not-required | Reference |
| RSRC-087 | — | Catalyst — monitoring / observability docs | P4 | not-required | Reference |
| RSRC-088 | — | Docker / containerization best practices | P4 | not-required | Reference |
| RSRC-089 | — | Graph database benchmark comparisons | P4 | not-required | Informs Neo4j decision |
| RSRC-090 | — | RAG system evaluation benchmarks | P4 | not-required | Informs Ask Berunda |
| RSRC-091 | R016 | RBI DBIE — macro-financial indicators | P4 | not-required | Optional context |
| RSRC-092 | — | Karnataka police beat / patrol zone maps (research) | P4 | not-required | Non-authoritative |

---

## 7. Category Summary

| Category | Present | Missing | Inaccessible | Not Required | Total |
|----------|---------|---------|--------------|--------------|-------|
| D1 — Official Datathon Material | 0 | 0 | 8 | 0 | 8 |
| D2 — Zoho Catalyst Platform | 0 | 7 | 0 | 0 | 7 |
| D3 — Crime & Public-Safety Stats | 0 | 8 | 0 | 2 | 10 |
| D4 — Geospatial Data | 0 | 7 | 0 | 3 | 10 |
| D5 — Census/Socio-Economic | 0 | 8 | 0 | 2 | 10 |
| D6 — Weather/Temporal | 0 | 7 | 0 | 3 | 10 |
| D7 — Legal References | 0 | 6 | 0 | 4 | 10 |
| D8 — Schemas/Standards | 0 | 0 | 0 | 5 | 5 |
| D9 — Repos/Systems | 0 | 8 | 0 | 2 | 10 |
| D10 — Research Papers | 0 | 0 | 0 | 5 | 5 |
| D11 — Frontend/Visualization | 0 | 5 | 0 | 0 | 5 |
| D12/D13 — Backend/Synthetic | 0 | 2 | 0 | 0 | 2 |
| D14 — Security/Governance | 0 | 0 | 0 | 5 | 5 |
| *Future integrations* | 0 | 0 | 0 | 17 | 17 |
| **Total** | **0** | **58** | **8** | **48** | **114** |

> [!NOTE]
> Total exceeds 92 because some RSRC entries appear in multiple category views.
> The unique resource count is 92. Inaccessible + Missing = Not Yet Verified (66)
> are the actionable items. Not-required (48) are explicitly out of acquisition scope.

---

## 8. Inventory by Acquisition Method

| Acquisition Method | Count | Resource Examples |
|--------------------|-------|-------------------|
| AUTO-API | 8 | RSRC-018, RSRC-022, RSRC-029 |
| AUTO-DIRECT-DOWNLOAD | 25 | RSRC-016, RSRC-032, RSRC-044 |
| AUTO-GIT | 6 | RSRC-040, RSRC-041, RSRC-044 |
| AUTO-BROWSER-WITH-USER-SESSION | 4 | RSRC-003, RSRC-004, RSRC-005 |
| SEMI-AUTOMATED | 5 | RSRC-024, RSRC-030, RSRC-031 |
| MANUAL-AUTHORIZED | 8 | RSRC-001, RSRC-025, RSRC-046 |
| FUTURE-RESTRICTED | 17 | RSRC-064–080 |
| DO-NOT-ACQUIRE | 19 | RSRC-036–039, RSRC-048–051, RSRC-081–092 |
| **Total** | **92** | |

---

*This report is auto-generated from `manifests/resource_manifest.csv`.*
