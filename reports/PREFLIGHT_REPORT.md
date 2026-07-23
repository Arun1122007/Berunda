# Preflight Report

> **Generated:** 2026-07-18T10:10:00+05:30
> **Workspace:** d:\Hack2Skill\Berunda
> **Status:** COMPLETE

---

## 1. Environment

| Tool | Version |
|------|---------|
| OS | Windows 11 (10.0.26100) |
| PowerShell | 5.1.26100.8875 |
| Python | 3.13.5 |
| Git | 2.52.0.windows.1 |
| Node.js | v24.15.0 |
| Java | 19.0.1 |
| pip | 26.1.2 |

## 2. Disk Space

| Drive | Free (GB) | Used (GB) |
|-------|-----------|-----------|
| C: | 18.87 | 163.83 |
| D: | 107.68 | 185.29 |

Workspace is on D: — 107.68 GB free is ample for all planned acquisitions.

## 3. Git State

| Field | Value |
|-------|-------|
| Branch | main |
| Commit | 629c030 |
| Remote | https://github.com/Arun1122007/Berunda.git |
| Tag | `pre-acquisition-scaffold` |
| Status | Clean (checkpoint committed) |

## 4. Existing Data Files

R001 (ERD) is present at `blueprints/h2s/Police_FIR_ER_Diagram.pdf` (491,459 bytes).
No other data/resource files exist yet — directories created but empty.

## 5. Python Packages

**Installed:** pandas==2.3.1, requests==2.32.4, networkx==3.6.1

**Now installed:** Faker==40.31.0, shapely==2.1.2, geopandas==1.1.4

## 6. Manifest Files

| File | Status |
|------|--------|
| resource_manifest.csv | Created (92 resources) |
| resource_manifest.json | Created (35 resources — schema differs from CSV) |
| download_manifest.csv | Created (populated) |
| repository_inventory.csv | Created (populated) |
| license_inventory.csv | Created (31 entries) |
| provenance.jsonl | Created (16 provenance entries) |
| failure_log.csv | Created (populated) |
| missing_resource_register.csv | Created (5 blocked items) |
| approval_register.csv | Created (empty template) |

## 7. Domain Allowlist

The following 19 domains are approved for automated access:

- `hack2skill.com`
- `catalyst.zoho.com`
- `help.catalyst.zoho.com`
- `ncrb.gov.in`
- `data.gov.in`
- `ksp.karnataka.gov.in`
- `ndap.niti.gov.in`
- `overpass-api.de`
- `bhuvan.nrsc.gov.in`
- `censusindia.gov.in`
- `open-meteo.com`
- `indiacode.nic.in`
- `bprd.nic.in`
- `github.com`
- `js.cytoscape.org`
- `pypi.org`
- `npmjs.com`
- `owasp.org`
- `nist.gov`

## 8. Acquisition Plan (Dry Run)

### P0 — Competition-Critical (Immediate)
- [x] R001 — ERD/DB Design Doc (**already in hand**)
- [ ] R002 — Challenge rules (**blocked — needs browser session**)
- [ ] R003 — Catalyst credits (**blocked — needs manual console action**)
- [ ] R006 — NCRB Crime in India reports
- [ ] R020 — BNS 2023 text

### P1 — Prototype-Critical (First 3 Days)
- [ ] R004, R005 — Catalyst docs (bookmark, don't archive)
- [ ] R008 — KSP Monthly Crime Review PDFs
- [ ] R011 — OSM Overpass API (Karnataka POIs)
- [ ] R012 — Bhuvan WMS layers
- [ ] R017 — Open-Meteo historical weather
- [ ] R021 — BNSS & BSA texts
- [ ] R022 — DPDP Act & Rules
- [ ] R026 — FollowTheMoney repo (reference)
- [ ] R027 — Kepler.gl repo (reference)
- [ ] R032 — Faker (`pip install Faker`)

### P2 — Enterprise-Enrichment (First Week)
- [ ] R007 — NCRB OGD data
- [ ] R009, R015 — NDAP datasets
- [ ] R014 — Census of India
- [ ] R019 — ECI election dates
- [ ] R028 — Neo4j CE
- [x] R029 — NetworkX (**already installed**)
- [ ] R030 — MapLibre GL JS (npm)
- [ ] R031 — Cytoscape.js (npm)

### Blocked (Human Action Required)
- R002 — Login to Hack2Skill dashboard
- R003 — Redeem Catalyst credits in console
- R013 — Survey of India licensing check
- R018 — IMD bulk access verification
- R033 — indic-faker source verification

### Excluded (DO-NOT-ACQUIRE / FUTURE-RESTRICTED)
- R010 — Karnataka Police Citizen Portal (UX ref only)
- R016 — RBI DBIE (P4, not needed)
- R023-R025 — P4 research/standards (defer)

---

## 9. Recommendations

1. Run `pip install Faker shapely` before starting acquisition scripts
2. Manually access Hack2Skill dashboard to confirm R002 submission format
3. Redeem Catalyst credits (R003) immediately — code is time-limited
4. Begin P0/P1 automated acquisition after this preflight is approved

---

*End of Preflight Report*
