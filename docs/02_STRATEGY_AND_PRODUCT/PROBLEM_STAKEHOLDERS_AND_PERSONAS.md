# Problem, Stakeholders, and Personas

[//]: # (Document ID: BERUNDA-PERS-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint | Last Verified: 2026-07-17 | Review: Monthly)

---

## Problem Statement

### Current State

Karnataka State Police manages crime data through a combination of:
- Station-level Excel sheets maintained independently at each police station
- CCTNS entries for digitized FIRs
- Quarterly/annual reports compiled manually by SCRB

This creates four systemic failures:

1. **Data silos** — No cross-station or cross-district view of crime patterns
2. **No relationship intelligence** — The source schema (FIR ERD) scopes `Accused` and `Victim` records per-case, with no native cross-case identity. A person appearing in multiple FIRs generates independent, unlinked records
3. **Reactive posture** — Without pattern discovery, resource allocation happens after crime spikes
4. **SCRB blindness** — The state bureau receives fragments, not a live structured feed

### Target State

A single intelligence platform where:
- Raw FIR data is ingested and normalized in real time
- Persons, vehicles, and locations are automatically resolved across cases
- Analysts see spatiotemporal hotspots with time-layered patterns
- Investigators see relationship graphs with hidden-link discovery
- Anyone can ask natural-language questions and get grounded, cited answers

## Stakeholders

| STK-ID | Stakeholder | Primary Need | Priority |
|--------|-------------|--------------|----------|
| STK-001 | Investigating Officers (IOs) | Fast cross-referencing of suspects/vehicles/locations across cases | MUST |
| STK-002 | Station House Officers (SHOs) | Local dashboard for jurisdiction awareness | MUST |
| STK-003 | SCRB Analysts | State-wide drillable analytics, trend alerts, statutory reporting | MUST |
| STK-004 | Superintendent of Police (District) | Resource deployment recommendations, hotspot maps | MUST |
| STK-005 | Cyber Crime Cells | OSINT and digital-evidence correlation | VISION |
| STK-006 | Forensic Labs | Evidence metadata linkage, chain-of-custody tracking | VISION |
| STK-007 | Judiciary / Courts | Structured case timelines (read-only, access-controlled) | VISION |
| STK-008 | DGP Office / Home Ministry | State-level KPI dashboards | SHOULD |
| STK-009 | Women Safety Wing | Crime-against-women pattern and hotspot views | SHOULD |
| STK-010 | Traffic Police | Vehicle-linked incident cross-referencing | SHOULD |
| STK-011 | Citizens (indirect) | Faster resolution, transparent governance safeguards | SHOULD |
| STK-012 | Governance / Compliance Officer | Fairness audit, bias monitoring, statutory reporting | MUST |

## Personas

### Persona 1: Inspector Ananya (IO — Primary Investigator)

- **Role:** Investigating Officer, Bengaluru City Police
- **Daily context:** Reviews 3-5 new FIRs daily. Spends hours manually cross-referencing suspect names against prior cases using Excel filters
- **Pain points:** No way to know if "Suresh Kumar" accused in today's FIR is the same person in three prior cases from different stations
- **Needs from Berunda:** Entity resolution that automatically surfaces prior involvements; relationship graph showing connections; "Ask Berunda" for quick case queries
- **Success metric:** Time to see all prior incidents connected to a suspect reduced from hours to minutes

### Persona 2: SHO Ramesh (Station House Officer)

- **Role:** In charge of a police station in Mysuru district
- **Daily context:** Responsible for overall crime trends in jurisdiction. Submits monthly reports to SP office
- **Pain points:** No real-time view of emerging crime patterns; relies on Excel pivot tables
- **Needs from Berunda:** Local dashboard showing current crime trends; hotspot map for patrol deployment; anomaly alerts for unusual spikes
- **Success metric:** Can identify emerging crime patterns in jurisdiction within one dashboard view

### Persona 3: SCRB Analyst Priya

- **Role:** Data analyst at State Crime Records Bureau
- **Daily context:** Compiles district-wise crime statistics from station reports; prepares quarterly trend analyses
- **Pain points:** Manual data collection from stations; inconsistent formats; no live state-wide view
- **Needs from Berunda:** State command view with drill-down; automated report generation; cross-district comparison
- **Success metric:** Statutory reports generated directly from platform, not manual Excel compilation

### Persona 4: Governance Officer Krishnamurthy

- **Role:** Compliance and oversight role
- **Daily context:** Ensures AI recommendations are fair and auditable; monitors for bias
- **Pain points:** No tools to verify that predictive models don't use protected characteristics
- **Needs from Berunda:** Fairness dashboard showing score distributions; audit log search; feature-importance review
- **Success metric:** Can confirm on demand that no model uses caste/religion features
