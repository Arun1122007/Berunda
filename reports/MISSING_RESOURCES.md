# Missing Resources — Gap Analysis

> **Generated:** 2026-07-18
> **Measured against:** Blueprint Section C (35 resources) + Section E (Feature-to-Data Matrix)

---

## High-Priority Gaps (P0/P1)

| ID | Resource | Impact | Mitigation |
|----|----------|--------|------------|
| R002 | Challenge rules/submission format | **CRITICAL** — submission format unknown | User must log into Hack2Skill dashboard |
| R003 | Catalyst credits | **CRITICAL** — cannot deploy without credits | User must redeem at catalyst.zoho.com |
| R006 | NCRB Crime in India reports | Validation baseline missing | Download from ncrb.gov.in |
| R008 | KSP Monthly Crime Review | State-level baseline missing | Download from ksp.karnataka.gov.in |
| R011 | OpenStreetMap POIs | Hotspot map POI enrichment missing | Run Overpass API query |
| R012 | Bhuvan WMS layers | Terrain/satellite layers missing | Check registration requirements |
| R017 | Open-Meteo weather | Weather feature input missing | API query needed |
| R020 | BNS 2023 text | Legal classification reference missing | Download from indiacode.nic.in |
| R021 | BNSS & BSA | Procedural law reference missing | Download from indiacode.nic.in |
| R022 | DPDP Act & Rules | Compliance framing missing | Download from indiacode.nic.in |
| R032 | Faker (en_IN) | Cannot generate synthetic data | `pip install Faker` |

## Blocked Resources (Human Action Required)

| ID | Resource | Blocker | Action |
|----|----------|---------|--------|
| R002 | Hack2Skill dashboard | Login required | Open browser, log in, record submission format |
| R003 | Catalyst credits | Console action required | Visit catalyst.zoho.com, redeem promo code KSPH26 |
| R013 | Survey of India boundaries | Licensing unverified | Check surveyofindia.gov.in terms |
| R018 | IMD weather data | Bulk access method unclear | Investigate mausam.imd.gov.in |
| R033 | indic-faker | Source/repo unverified | Search PyPI/GitHub for exact package |

## Feature Impact Assessment

| Feature | Missing Data | Impact Level | Can Demo Without? |
|---------|-------------|--------------|-------------------|
| Trend dashboards | R006, R008 baselines | Medium | ✅ Yes — use synthetic distribution |
| Hotspot map | R011 POIs, R012 terrain | Medium | ✅ Yes — map works, enrichment missing |
| Weather context | R017 | Low | ✅ Yes — feature disabled for demo |
| Legal classification | R020-R022 | High | ⚠️ Partial — generic section labels |
| Synthetic data | R032 Faker | **Critical** | ❌ No — need Faker to generate data |
| Ask Berunda | R004-R005 Catalyst docs | Medium | ✅ Yes — can use QuickML without full docs |

---

## Recommended Immediate Actions

1. `pip install Faker` — unblocks synthetic data generation (Day 1 dependency)
2. User: log into Hack2Skill, record submission requirements
3. User: redeem Catalyst credits
4. Run: `python scripts/acquisition/download_resources.py --no-dry-run --priority P0`
5. Run: `python scripts/acquisition/download_resources.py --no-dry-run --priority P1`
