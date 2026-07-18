# Executive Summary

[//]: # (Document ID: BERUNDA-EXEC-001 | Version: 1.0 | Status: DRAFT | Classification: PUBLIC | Owner: Berunda Team | Audience: Team | Source: 01_Enterprise_Blueprint | Last Verified: 2026-07-17 | Review: Monthly)

---

## Problem

Karnataka's State Crime Records Bureau (SCRB) manages crime data in station-level Excel silos. There is no systematic link analysis, no AI-driven pattern discovery, and no proactive tooling. A suspect involved in five incidents across three districts currently appears as five unrelated case files. Patrol deployment happens reactively, after crime spikes.

## Solution

Project Berunda is an AI-native crime intelligence platform that turns fragmented FIR records into a connected, queryable intelligence layer. Built entirely on the mandatory Zoho Catalyst stack, it provides:

1. **Cross-case entity resolution** — linking persons, vehicles, and locations across cases when the source schema contains no native cross-case identity
2. **Explainable, bias-audited risk scoring** — every score ships with a visible feature-importance breakdown; caste and religion fields are hard-excluded from all models
3. **Geospatial hotspot detection** — district-to-station drill-down with temporal patterns and anomaly alerts
4. **Relationship graph analysis** — surfacing hidden connections between cases that isolated records miss
5. **Grounded natural-language investigation assistance** — "Ask Berunda" gives cited answers over a curated case corpus
6. **Live fairness governance** — verifiable exclusion of sensitive fields, auditable at any time

## Differentiation

Unlike existing systems (CCTNS, Palantir Gotham, IBM i2, PredPol), Berunda is simultaneously:
- Open-source and state-owned
- Natively bilingual for Karnataka (Kannada + English)
- Designed with bias auditing as a first-class architectural control, not an add-on

## MVP Impact

| Stakeholder | Impact |
|-------------|--------|
| Investigators | Minutes instead of days to see every prior incident connected to a suspect |
| SCRB | A live, drillable state map instead of a quarterly PDF |
| Citizens | Faster case resolution with transparent governance safeguards |
| Government | An open-core system Karnataka can own and extend |

## Feasibility

2-person team, 11 days, 12 BUILDABLE features, mandatory Catalyst deployment. Full enterprise roadmap documented separately.
