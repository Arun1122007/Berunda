# AGENTS.md — Project Berunda Acquisition Agent Operating Instructions

> **Document ID:** BERUNDA-AGENTS-001 | **Version:** 1.0 | **Status:** ACTIVE
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-18

---

## Workspace Root

```
d:\Hack2Skill\Berunda
```

Remote: `https://github.com/Arun1122007/Berunda.git` (branch: `main`)

---

## Purpose

This file governs any AI agent or automated tool operating inside this workspace.
It summarizes the safety rules from `document/h2s/Project_Berunda_07_Autonomous_Agent_Prompt.md`
and must be read before any automated action.

---

## Non-Negotiable Safety Rules (Summary)

1. **Workspace-only** — never read, write, or delete anything outside `d:\Hack2Skill\Berunda`.
2. **No destructive recursion** — never `rm -rf` or `Remove-Item -Recurse -Force` without explicit user approval.
3. **No bypassing** — never bypass CAPTCHA, login walls, paywalls, `robots.txt`, rate limits, or ToS.
4. **No real PII** — never download or fabricate real biometric, telecom, banking, Aadhaar, or individual-level police data.
5. **No secrets in logs** — never print cookies, tokens, API keys, or credentials.
6. **No secrets in git** — never commit secrets or raw data to the public remote.
7. **Quarantine-first** — every download goes to `quarantine/` until validated.
8. **Dry-run default** — every acquisition script defaults to `--dry-run`.
9. **Human approval required** for: authenticated sessions, legal ToS click-throughs, files > 200 MB, total > 1 GB, system-wide installs, executing cloned code, uploads, paid APIs.
10. **Append-only logging** — every action logged to `logs/acquisition.log`.

---

## Domain Allowlist

Only these domains may be accessed by automated scripts. Any other domain requires explicit user approval.

| Domain | Purpose | Resources |
|--------|---------|-----------|
| `hack2skill.com` | Datathon dashboard (browser-only) | R002 |
| `catalyst.zoho.com` | Catalyst credits & console | R003 |
| `help.catalyst.zoho.com` | Catalyst documentation | R004, R005 |
| `ncrb.gov.in` | NCRB crime reports | R006 |
| `data.gov.in` | Open Government Data | R007 |
| `ksp.karnataka.gov.in` | Karnataka State Police | R008 |
| `ndap.niti.gov.in` | NITI Aayog NDAP | R009, R015 |
| `overpass-api.de` | OpenStreetMap Overpass | R011 |
| `bhuvan.nrsc.gov.in` | ISRO/NRSC Bhuvan | R012 |
| `censusindia.gov.in` | Census of India | R014 |
| `open-meteo.com` | Weather API | R017 |
| `indiacode.nic.in` | India Code (BNS/BNSS/BSA/DPDP) | R020-R022 |
| `bprd.nic.in` | BPRD handbook | R023 |
| `github.com` | Open-source repos | R026, R027, R030 |
| `js.cytoscape.org` | Cytoscape.js | R031 |
| `pypi.org` | Python packages | R029, R032 |
| `npmjs.com` | Node packages | R030, R031 |
| `owasp.org` | Security standards | R034 |
| `nist.gov` | NIST frameworks | R035 |

---

## Command Allowlist

| Command Pattern | Purpose |
|----------------|---------|
| `git clone --depth 1` | Shallow clone repos |
| `git tag`, `git log`, `git rev-parse` | Commit pinning |
| `pip install Faker networkx shapely geopandas` | Python dependencies |
| `npm install maplibre-gl cytoscape` | Frontend dependencies |
| `Invoke-WebRequest` / `curl` | File downloads (to quarantine/) |
| `python scripts/acquisition/*.py` | Acquisition scripts |
| `python scripts/validation/*.py` | Validation scripts |
| `certutil -hashfile` / `Get-FileHash` | Checksum verification |

---

## Status Labels

Use exactly these labels when reporting resource state:

- `completed` — downloaded, validated, and manifest entry created
- `partially completed` — downloaded but validation pending
- `blocked` — awaiting human approval or external dependency
- `manual action required` — cannot be automated
- `future restricted integration` — not acquired under this blueprint

---

## File Organization

See `document/h2s/Project_Berunda_06_Resource_Acquisition_Blueprint.md`, Section G for the
full directory structure specification.

---

## Contact

For questions about these rules, refer to the full Autonomous Agent Prompt at:
`document/h2s/Project_Berunda_07_Autonomous_Agent_Prompt.md`
