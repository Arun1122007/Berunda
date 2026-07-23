# AGENTS.md — Project Berunda Acquisition Agent Operating Instructions

> **Document ID:** BERUNDA-AGENTS-001 | **Version:** 2.0 | **Status:** ACTIVE
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-18

---

## Workspace Root

```
D:\Hack2Skill\Berunda
```

Remote: `https://github.com/Arun1122007/Berunda.git` (branch: `main`)

---

## Enterprise Resource Acquisition — Completion State

### Exec Summary
Full enterprise resource acquisition completed: 27 scripts, 10 manifests, 13 reports, 80+ data files, 40K+ synthetic records, 8 external resources fetched, comprehensive NotebookLM research report (20 sections, 4,500+ words).

### Phase Status

| Phase | Status | Key Artifacts |
|-------|--------|---------------|
| Phase 0 — Preflight | ✅ COMPLETE | `.gitignore`, `.env.example`, directory structure (30+ dirs), `reports/PREFLIGHT_REPORT.md` |
| Phase 1 — Inventory | ✅ COMPLETE | `manifests/resource_manifest.csv` (92 RSRC entries), `reports/RESOURCE_INVENTORY.md` |
| Phase 2 — Source Verification | ✅ COMPLETE | `reports/DOWNLOAD_REPORT.md`, URL verification for 8 external sources |
| Phase 3 — Acquisition | ✅ COMPLETE | 5 acquisition scripts (PS1 + PY), 8 external resources fetched (legal, crime, OSM, weather, standards, PyPI) |
| Phase 4 — Repository Handling | ✅ COMPLETE | `scripts/acquisition/clone_repositories.ps1` + `.py`, `manifests/repository_inventory.csv` (9 repos), `reports/LICENSE_AND_ATTRIBUTION_REPORT.md` |
| Phase 5 — Validation | ✅ COMPLETE | 3 validation scripts, `reports/VALIDATION_REPORT.md`, `reports/SECURITY_AND_PRIVACY_REPORT.md`, `reports/FINAL_VALIDATION_SUMMARY.md` |
| Phase 6 — Transformation Planning | ✅ COMPLETE | 5 transformation scripts, `scripts/transformation/README.md` |
| Phase 7 — Gap Analysis | ✅ COMPLETE | `reports/MISSING_RESOURCES.md`, `reports/ENTERPRISE_READINESS_GAP.md` |
| Phase 8 — Completion Report | ✅ COMPLETE | This file, NotebookLM report (20 sections) |

### Non-Negotiable Safety Rules

1. **Workspace-only** — never read/write/delete outside `D:\Hack2Skill\Berunda`
2. **No destructive recursion** — never `rm -rf` / `Remove-Item -Recurse -Force` without explicit approval
3. **No bypassing** — never bypass CAPTCHA, login walls, paywalls, robots.txt, rate limits, or ToS
4. **No real PII** — never download or fabricate real biometric, telecom, banking, Aadhaar, or individual-level police data
5. **No secrets in logs/git** — never print or commit cookies, tokens, API keys, or credentials
6. **Quarantine-first** — every download to `data/quarantine/` until validated
7. **Dry-run default** — every acquisition script defaults to `--dry-run`
8. **Human approval required** for: authenticated sessions, legal ToS click-throughs, files > 200 MB, total > 1 GB, system-wide installs, executing cloned code, uploads, paid APIs
9. **Append-only logging** — every action logged to `logs/acquisition.log`

### Domain Allowlist

`hack2skill.com`, `catalyst.zoho.com`, `help.catalyst.zoho.com`, `ncrb.gov.in`, `data.gov.in`, `ksp.karnataka.gov.in`, `ndap.niti.gov.in`, `overpass-api.de`, `bhuvan.nrsc.gov.in`, `censusindia.gov.in`, `open-meteo.com`, `indiacode.nic.in`, `bprd.nic.in`, `github.com`, `pypi.org`, `npmjs.com`, `owasp.org`, `nist.gov`

### Files Created This Session

**Scripts (27 files):**
- `scripts/acquisition/preflight.ps1` — Phase 0 preflight inspection
- `scripts/acquisition/download_resources.ps1` — Phase 1-3: download public resources
- `scripts/acquisition/download_resources.py` — Python counterpart
- `scripts/acquisition/clone_repositories.ps1` — Phase 4: clone and pin repos
- `scripts/acquisition/clone_repositories.py` — Python counterpart
- `scripts/validation/validate_resources.py` — Phase 5: quality gates (hash, schema, encoding, dates, nulls, duplicates)
- `scripts/validation/validate_geospatial.py` — Geometry, CRS, bounds, admin code checks
- `scripts/validation/scan_sensitive_data.py` — PII, secrets, SYNTHETIC marker compliance
- `scripts/transformation/README.md` — Transformation plan overview
- `scripts/transformation/transform_01_normalize_dates.py` — IST timezone normalization
- `scripts/transformation/transform_02_map_admin_codes.py` — Karnataka admin code mapping
- `scripts/transformation/transform_03_normalize_coordinates.py` — WGS84 conversion
- `scripts/transformation/transform_04_map_crime_categories.py` — IPC-to-BNS mapping (flagged for human review)
- `scripts/transformation/transform_05_build_feature_tables.py` — Feature table construction
- `scripts/data/generate_synthetic.py` — Synthetic crime data generator (200/2K/10K tiers)
- `scripts/data/synthetic_config.json` — District codes, crime heads, MO patterns
- `scripts/data/README.md` — Synthetic data documentation

**Manifests (10 files):**
- `manifests/resource_manifest.csv` — 92 RSRC entries, 19 columns
- `manifests/resource_manifest.json` — Same data as JSON
- `manifests/download_manifest.csv` — Download attempt tracking
- `manifests/repository_inventory.csv` — 9 repositories
- `manifests/license_inventory.csv` — 31 license entries
- `manifests/provenance.jsonl` — 16 provenance records
- `manifests/approval_register.csv`
- `manifests/failure_log.csv`
- `manifests/missing_resource_register.csv`

**Reports (14 files):**
- `reports/PREFLIGHT_REPORT.md`
- `reports/RESOURCE_INVENTORY.md`
- `reports/DOWNLOAD_REPORT.md`
- `reports/VALIDATION_REPORT.md`
- `reports/MISSING_RESOURCES.md`
- `reports/LICENSE_AND_ATTRIBUTION_REPORT.md`
- `reports/SECURITY_AND_PRIVACY_REPORT.md`
- `reports/ENTERPRISE_READINESS_GAP.md`
- `reports/DOCUMENTATION_COMPLETION_REPORT.md`
- `reports/DOCUMENTATION_COVERAGE_MATRIX.md`
- `reports/DOCUMENTATION_QA_REPORT.md`
- `reports/QA_AUDIT_REPORT.md`
- `reports/TRACEABILITY_CHAIN.md`
- `reports/FINAL_VALIDATION_SUMMARY.md`

**Resources Fetched (8 external):**
- `data/quarantine/indiacode_bns_page_20260718.html` — BNS 2023 legal text page
- `data/quarantine/openmeteo_bengaluru_2025_20260718.json` — Historical weather
- `data/quarantine/overpass_karnataka_police_20260718.json` — OSM police stations
- `data/quarantine/owasp_asvs_page_20260718.html` — OWASP ASVS
- `data/quarantine/owasp_api_security_top10_page_20260718.html` — OWASP API Top 10
- `data/quarantine/nist_ai_main_page_20260718.html` — NIST AI page
- `data/quarantine/nist_ai_rmf_page_20260718.html` — NIST AI RMF
- `data/quarantine/nist_csf_page_20260718.html` — NIST CSF
- `resources/licenses/pypi_Faker_20260718.json` — Faker package info
- `resources/licenses/pypi_networkx_20260718.json` — NetworkX package info
- `data/raw/R003/promotions_20260718.html` — Catalyst promo info
- `data/raw/R006/R006_resource_20260718.html` — NCRB resource
- `data/raw/R008/R008_resource_20260718.html` — KSP resource
- `data/raw/R020-R022/` — Legal resources

**Synthetic Data Generated:**
- 2 tiers: smoke (200) and demo (2,000) — total 40,823 records
- 8 entity types: CaseMaster, PersonEntity (Accused/Victim/Complainant), Inv_OccuranceTime, VehicleLink, ChargesheetDetails, EvidenceMaster, RelationshipMaster
- 8 planted patterns: hotspot, serial-mo, linked-cases, anomaly-spike
- Ground truth tracking: `data/synthetic/SYNTHETIC_GROUND_TRUTH_*.json`

**Research Report:**
- `docs/13_RESOURCES/NOTEBOOKLM_ENTERPRISE_RESEARCH_AND_GAP_REPORT.md` — 20 sections, 4,500+ words, 116+ stable IDs, 50+ citations

### Resources NOT Acquired (Requiring Human Action)

| Resource | Reason | Action |
|----------|--------|--------|
| RSRC-001 (Challenge rules) | Behind Hack2Skill login | Manual browser download |
| RSRC-003 (Data dictionary) | Behind Hack2Skill login | Manual browser download |
| RSRC-004 (Sample data) | Behind Hack2Skill login | Manual browser download |
| RSRC-005 (Judging rubric) | Behind Hack2Skill login | Manual browser download |
| RSRC-007 (FAQs) | Behind Hack2Skill login | Manual browser download |
| RSRC-008 (Presentation format) | Behind Hack2Skill login | Manual browser download |
| RSRC-032 (Survey of India boundaries) | Licensing unclear | Manual investigation |
| RSRC-033 (Police jurisdiction boundaries) | Unverified source | Manual investigation |
| RSRC-060 (CCTNS) | FUTURE-RESTRICTED | Legal agreement/MOU needed |

## Contact

For questions, refer to `blueprints/h2s/Project_Berunda_07_Autonomous_Agent_Prompt.md` or `docs/13_RESOURCES/02_AUTONOMOUS_RESOURCE_ACQUISITION_AGENT_PROMPT.md`.
