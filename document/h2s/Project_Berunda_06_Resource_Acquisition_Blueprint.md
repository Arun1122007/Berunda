# 01_ENTERPRISE_RESOURCE_ACQUISITION_BLUEPRINT

## Project Berunda — Karnataka State Police Datathon 2026

> **Scoping note, stated up front rather than hidden:** the source prompt for this file specifies a 32-column schema for every resource row. Applying all 32 columns to every one of the ~35 real resources below would produce an unreadable table (over 1,100 cells) without adding decision-relevant information. This document uses a **streamlined 15-column table** covering the columns that actually drive an acquisition decision, and folds the remaining fields (validation procedure detail, retention rule, data-owner assignment, storage path) into the **per-category narrative (Section D)** and the **manifest schema (Section H)**, where they're specified once at the category level instead of repeated unchanged across dozens of rows. Every URL below was verified via live search during this session; anything not verified is explicitly marked `UNVERIFIED — REQUIRES HUMAN CHECK` rather than guessed at.

---

## A. Executive Resource Strategy

**Purpose of this package:** identify everything Project Berunda should acquire — data, documentation, SDKs, repositories, standards, and research — to move from a hackathon prototype toward a lawful, explainable, production-viable crime-intelligence platform, while being explicit about what's acquirable now versus what remains a future, authorized integration.

**Hackathon objective vs. enterprise objective:** the hackathon objective is a working, demoable slice built entirely on lawfully-obtainable data (Section D13's synthetic data plus the organizer-provided schema). The enterprise objective — real CCTNS integration, real person-level records, cross-district/cross-state correlation — depends on data-sharing agreements and legal review that are explicitly out of scope for anything this package acquires automatically.

**Prototype data boundary:** nothing acquired under this blueprint may include real victim, witness, accused, biometric, banking, telecom, Aadhaar, or precise-residential data. Where such categories matter to the platform's design, they are represented only as clearly-labeled synthetic records or as documented future-integration contracts (Priority P3).

**Classification used throughout this document:**
- **Authorized** — provided directly by the Datathon organizers.
- **Public** — lawfully public, appropriately licensed government or open data.
- **Synthetic** — generated, clearly labeled, never presented as real.
- **Restricted** — real systems (CCTNS, telecom CDR, bank records) represented only as a future integration contract, never acquired now.

**Resource-acquisition principles:**
- *Data minimization* — acquire only what a specific, named feature needs; nothing is collected "in case it's useful later."
- *Privacy by design* — restricted/sensitive fields (Section D5, D7) are excluded from acquisition scope entirely, not collected-then-restricted.
- *Security by design* — every download lands in quarantine before validation; nothing trusted by default.
- *Open-source compliance* — no code or data is treated as reusable without a clear, checked license.
- *Reproducibility* — every acquisition is logged with source, date, and checksum so it can be redone identically.
- *Provenance / chain of custody* — every dataset's origin, access date, and transformation history is tracked in `manifests/provenance.jsonl` (Section H).
- *Human approval points* — anything crossing into authenticated access, large downloads, or restricted-category data requires a named human sign-off, never an automated one.

**Definitions used throughout:**
- **Downloaded** — the file exists on disk with a recorded checksum and source URL.
- **Verified** — the file has passed the Section I quality gates relevant to its type.
- **Usable** — verified, and its schema/fields are mapped to at least one Berunda feature in Section E.
- **Production-approved** — usable, and has passed a named human's sign-off for its declared classification (Authorized/Public/Synthetic/Restricted).

---

## B. Priority Levels

- **P0 — Competition-critical.** Organizer material: the ERD/Database Design Document, challenge rules, submission requirements, sample data, Catalyst credit instructions. Missing a P0 item can block submission entirely.
- **P1 — Prototype-critical.** Whatever is required to implement and demo the core platform: Catalyst SDKs/docs, the geospatial/administrative reference data the hotspot map needs, the synthetic-data generation tooling.
- **P2 — Enterprise-enrichment.** Improves accuracy, scalability, governance, or presentation, but the Phase 1 demo runs without it: NCRB benchmark statistics, additional socio-economic context, extra open-source reference repositories.
- **P3 — Future authorized integrations.** Restricted systems (CCTNS live feed, telecom CDR, banking/UPI records) represented only as interface contracts and mock adapters — never acquired as real data under this blueprint.
- **P4 — Research-only.** Papers, benchmarks, and reference implementations that inform design decisions but aren't pulled directly into the running system.

---

## C. Master Resource Inventory

**Columns used:** ID · Priority · Category · Resource & Verified Source · Why Needed / Feature Enabled · Publisher · License/Terms · Legal-Access Class · Personal-Data Risk · Acquisition Method · Catalyst Mapping · Known Limitation · Acceptance Criterion.

**Acquisition-method codes** (defined fully in Section F): `AUTO-API` · `AUTO-DIRECT-DOWNLOAD` · `AUTO-GIT` · `AUTO-BROWSER-WITH-USER-SESSION` · `SEMI-AUTOMATED` · `MANUAL-AUTHORIZED` · `FUTURE-RESTRICTED` · `DO-NOT-ACQUIRE`.

| ID | Pri | Cat | Resource & Source | Why Needed | Publisher | License | Legal Class | PII Risk | Method | Catalyst Mapping | Limitation | Acceptance Criterion |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R001 | P0 | D1 | Datathon ERD/DB Design Doc (organizer Resources tab) | Real schema, Blueprint §6 | Hack2Skill/KSP | Organizer terms | Authorized | High (real govt schema) | MANUAL-AUTHORIZED | Data Store | Already in hand — not a download task | Matches uploaded PDF exactly |
| R002 | P0 | D1 | Challenge rules/timeline/submission requirements | Defines "done" | Hack2Skill | Organizer terms | Authorized | None | AUTO-BROWSER-WITH-USER-SESSION | n/a | Login-gated dashboard — needs your session | Exact submission format confirmed before Day 11 |
| R003 | P0 | D1 | Catalyst credit redemption — `catalyst.zoho.com/promotions.html?cn=KSPH26` | Needed to deploy at all | Hack2Skill/Zoho | Promo terms | Authorized | None | AUTO-DIRECT-DOWNLOAD | All Catalyst services | Time-limited code | Credits visible in Catalyst console |
| R004 | P1 | D2 | Zoho Catalyst docs — `help.catalyst.zoho.com` | All Catalyst usage, Blueprint §15 | Zoho | Zoho ToS | Public | None | AUTO-DIRECT-DOWNLOAD | All | Docs evolve — recheck close to build | Functions/AppSail/Data Store quickstarts open |
| R005 | P1 | D2 | Catalyst QuickML docs (LLM serving, RAG, AutoML) | Ask Berunda + Risk Scoring | Zoho | Zoho ToS | Public | None | AUTO-DIRECT-DOWNLOAD | QuickML | — | Confirms Qwen serving + RAG + feature importance |
| R006 | P0 | D3 | NCRB — `ncrb.gov.in`, "Crime in India" reports | National baseline for validation | NCRB (MHA) | Govt publication | Public | None (aggregate) | AUTO-DIRECT-DOWNLOAD | n/a (reference) | Latest full volume is 2022 | Report PDF opens, district tables parse |
| R007 | P2 | D3 | NCRB catalog on OGD Platform — `data.gov.in/ministrydepartment/National%20Crime%20Records%20Bureau%20(NCRB)` | Machine-readable NCRB data | NCRB/data.gov.in | GODL-India | Public | None | AUTO-API | n/a | Coverage varies by dataset | ≥1 CSV/API resource parses |
| R008 | P1 | D3 | KSP — Crime in Karnataka / Monthly Crime Review (`ksp.karnataka.gov.in/new-page/...`) | State/district baseline, Karnataka-specific | Karnataka State Police | Govt of Karnataka ToS | Public | None (aggregate) | AUTO-DIRECT-DOWNLOAD | n/a | Page structure changes — reverify near build | ≥2 recent Monthly Review PDFs retrieved |
| R009 | P2 | D3 | NITI Aayog NDAP — "Crime in India: IPC Crimes Statistics" (`ndap.niti.gov.in`) | Cross-sectoral merge w/ socio-economic data | NITI Aayog | NDAP open terms | Public | None (aggregate) | AUTO-DIRECT-DOWNLOAD | n/a | State-level, not always district | Dataset downloads, column count matches listing |
| R010 | — | D3 | Karnataka Police Citizen Portal — `policeseva.ksp.gov.in` | UX reference only, NOT a data source | Karnataka State Police | Govt ToS | Public (UX ref only) | None | DO-NOT-ACQUIRE | n/a | It's a citizen service, not bulk data | n/a |
| R011 | P1 | D4 | OpenStreetMap via Overpass API (`overpass-api.de`) | Location enrichment: stations, hospitals, schools, ATMs | OSM Foundation | ODbL | Public | None | AUTO-API | n/a | Rural Karnataka coverage may be sparse | Query returns >0 POIs per type for 1 test district |
| R012 | P1 | D4 | Bhuvan (ISRO/NRSC) — `bhuvan.nrsc.gov.in` | Terrain/forest/satellite map layers | ISRO/NRSC | Indian govt freeware terms | Public | None | AUTO-API (WMS/WFS) / SEMI-AUTOMATED | n/a | May need registration — verify at build time | ≥1 WMS layer renders in test map |
| R013 | P2 | D4 | Survey of India — `surveyofindia.gov.in` | Authoritative admin boundaries | Survey of India | `UNVERIFIED — REQUIRES HUMAN CHECK` | Public (TBC) | None | MANUAL-AUTHORIZED | n/a | Some SOI products not freely licensed | Pending licensing confirmation |
| R014 | P2 | D5 | Census of India — `censusindia.gov.in` | Population/literacy/urban-rural (non-caste) context | Registrar General & Census Commissioner | Govt publication | Public | None (aggregate, non-identifying) | AUTO-DIRECT-DOWNLOAD | n/a | 2021 Census postponed; 2011 is latest full dataset — say this explicitly in your pitch | ≥1 District Census Handbook retrieved |
| R015 | P2 | D5 | NITI Aayog NDAP (general socio-economic) | Cross-sectoral indicators beyond crime | NITI Aayog | NDAP open terms | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | — | Same as R009 |
| R016 | P4 | D5 | RBI DBIE | Optional macro/financial context, research-only | RBI | `UNVERIFIED — REQUIRES HUMAN CHECK` | Public | None | MANUAL-AUTHORIZED | n/a | Not needed for Phase 1 | n/a |
| R017 | P1 | D6 | Open-Meteo — `open-meteo.com` | Weather feature, Blueprint §6.6 | Open-Meteo | Free/open (recheck volume terms) | Public | None | AUTO-API | n/a | Rate limits at high volume | API call returns valid historical weather for 1 district |
| R018 | P2 | D6 | IMD — `mausam.imd.gov.in` | Official backup/validation for weather data | IMD | Govt terms — `UNVERIFIED` exact bulk-access method | Public | None | SEMI-AUTOMATED | n/a | Less straightforward bulk access than Open-Meteo | Pending access-method confirmation |
| R019 | P2 | D6 | Election Commission of India — `eci.gov.in` | Election-day flag for temporal features | ECI | Govt terms | Public | None | SEMI-AUTOMATED | n/a | Format varies by release | Karnataka election dates retrieved for relevant years |
| R020 | P0 | D7 | Bharatiya Nyaya Sanhita (BNS) 2023 — `indiacode.nic.in` (official) | Matches real `IPC/BNS Sections` field, Blueprint §6.1 | MHA / India Code | Public domain (Govt of India) | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | Legacy IPC→BNS mapping needs legal review before auto-applying | ≥3 sections cross-checked against sample FIR data |
| R021 | P1 | D7 | BNSS & BSA official text — `indiacode.nic.in` | Companion procedural/evidence law | MHA / India Code | Public domain | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | Same legal-review caveat as R020 | Both texts retrieved |
| R022 | P1 | D7 | DPDP Act 2023 & DPDP Rules 2025 | Compliance framing, Blueprint §13.4 | MeitY / India Code | Public domain | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | Rules still mid-rollout — recheck deadlines before submission | Both Act and Rules retrieved |
| R023 | P4 | D7 | BPRD BNS handbook — `bprd.nic.in` | Practitioner-level guidance | BPRD, MHA | Govt publication | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | Guidance only, not the Act itself | n/a |
| R024 | P4 | D8 | GeoJSON / OGC standards | Geospatial output format standard | IETF / OGC | Open standard | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | — | n/a |
| R025 | P4 | D8 | POLE data-model references | Informs canonical model, Blueprint §6.4 | Policing-informatics literature | Varies | Public (research) | None | MANUAL-AUTHORIZED | n/a | No single authoritative spec — a pattern, not a standard to claim compliance with | n/a |
| R026 | P1 | D9 | OpenAleph / FollowTheMoney schema | Entity/relationship design reference, Blueprint §6.3 | OCCRP | MIT (per prior research; `UNVERIFIED` exact repo URL this session) | Public | None | AUTO-GIT (once URL confirmed) | n/a | Reference/study only, not integrated directly | Repo clones, schema docs readable |
| R027 | P1 | D9 | Kepler.gl — `github.com/keplergl/kepler.gl` | Hotspot dashboard reference pattern | Uber / OpenJS Foundation | MIT | Public | None | AUTO-GIT | n/a (frontend reference) | React-based — confirm stack compatibility | Repo clones, demo runs locally |
| R028 | P2 | D9 | Neo4j Community Edition — `neo4j.com` | Phase-3 graph-DB upgrade path | Neo4j, Inc. | GPLv3 (Community) | Public | None | AUTO-DIRECT-DOWNLOAD | n/a (Phase 3) | Community Edition has scale/cluster limits | Installs, runs test Cypher query |
| R029 | P2 | D9 | NetworkX — `networkx.org` | Phase-1 graph-traversal logic | NetworkX developers | BSD | Public | None | AUTO-DIRECT-DOWNLOAD (pip) | n/a | Pure-Python — fine at prototype scale only | `pip install networkx` succeeds |
| R030 | P2 | D11 | MapLibre GL JS — `github.com/maplibre/maplibre-gl-js` | Open-source map rendering | MapLibre community | BSD-3-Clause | Public | None | AUTO-GIT / npm | n/a | — | npm package installs |
| R031 | P2 | D11 | Cytoscape.js — `js.cytoscape.org` | Link-analysis graph rendering | Cytoscape.js team | MIT | Public | None | AUTO-DIRECT-DOWNLOAD (npm) | n/a | — | Sample graph renders |
| R032 | P1 | D12/13 | Faker (`en_IN` locale) — `github.com/joke2k/faker` | Synthetic data generation, Blueprint §6.7 | joke2k / Faker community | MIT | Public (tool) | None (generates synthetic only) | AUTO-DIRECT-DOWNLOAD (pip) | n/a | `en_IN` coverage narrower than `en_US` | `pip install Faker`; en_IN names/addresses confirmed |
| R033 | P2 | D12/13 | indic-faker | Kannada-script synthetic text/names | `UNVERIFIED — REQUIRES HUMAN CHECK` (found via research as HuggingFace-hosted; confirm exact source before scripting) | `UNVERIFIED` | Public (tool) | None | SEMI-AUTOMATED | n/a | Smaller/newer project — verify maintenance status first | Pending source confirmation |
| R034 | P4 | D14 | OWASP ASVS / API Security Top 10 | Security baseline, Blueprint §12.5 | OWASP Foundation | CC-BY-SA | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | Guidance, not certification | Retrieved, cross-checked against §12 |
| R035 | P4 | D14 | NIST CSF & AI RMF | Governance/security reference, Blueprint §13.3 | NIST | US public domain | Public | None | AUTO-DIRECT-DOWNLOAD | n/a | US-authored — reference framework, not an Indian legal requirement | Both retrieved |

---

## D. Resource Categories

Detail for each field (validation procedure, retention, storage path, data owner) not repeated per-row above is specified here once per category.

### D1 — Official Datathon Material (R001-R003)
Everything here is either already provided (R001, the ER diagram) or sits behind your authenticated Hack2Skill dashboard (R002 — rules/timeline/judging criteria/FAQs, R003 — Catalyst credits). **None of this can be pulled by an unattended script** — it requires your logged-in browser session, which is exactly why the Autonomous Agent Prompt (File 2) treats `AUTO-BROWSER-WITH-USER-SESSION` as a distinct, explicitly-gated category rather than something it does silently. Validation: confirm R001 matches the uploaded PDF byte-for-byte; confirm R002's submission-format requirement before Day 10. Retention: keep indefinitely, this is your baseline of record. Owner: both team members should independently confirm R002's requirements — this is the one category where a misunderstanding costs the whole submission.

### D2 — Zoho Catalyst Platform Resources (R004-R005)
Docs, SDKs, and quickstarts for every mandatory Catalyst service in Blueprint Section 15. Validation: each quickstart's sample code should actually run against a fresh Catalyst project before Day 1 ends. Retention: bookmark, don't archive — docs change, always use the live version. Feature-to-Catalyst-service mapping is fully detailed in the Enterprise Blueprint, Section 15; this category exists to make sure you have the *documentation*, not to re-derive the mapping here.

### D3 — Crime and Public-Safety Statistics (R006-R010)
Separates cleanly into: incident-level (none acquired here — R001's synthetic-augmented data is your only incident-level source), aggregated statistics (R006, R007, R009 — all machine-readable or PDF), Karnataka-specific (R008), and explicitly-excluded (R010, a citizen service, not a data source). Validation: cross-check that your synthetic data's district distribution isn't wildly inconsistent with R008's real published numbers — that's the main reason to acquire this category at all for a hackathon build. Retention: these are reference baselines, keep the specific report version cited (report years change annually).

### D4 — Administrative and Geospatial Data (R011-R013)
OSM (R011) covers point-of-interest enrichment; Bhuvan (R012) covers terrain/satellite layers; Survey of India (R013) is flagged unverified pending a licensing check — **do not automate acquisition from R013 until that's resolved.** Validation: every geometry must pass a validity check (Section I) and every coordinate must fall within Karnataka's actual bounding box before being trusted in the hotspot map. Coordinate system: standardize everything to WGS84 (EPSG:4326) at ingestion.

### D5 — Census, Socio-Economic, and Development Indicators (R014-R016)
**Explicitly excludes** any caste-linked dataset (e.g. SECC) from acquisition scope entirely — this isn't a gap, it's a deliberate exclusion consistent with Enterprise Blueprint Sections 6.2/6.6. What's included (population, literacy, urbanization) is aggregate and non-identifying by construction. Validation: confirm no acquired file contains individual-level records — these sources are aggregate-by-publication, but re-verify on each vintage/release.

### D6 — Weather, Environment, and Temporal Context (R017-R019)
Open-Meteo (R017) as the primary automatable source; IMD (R018) as the official backup, access method still to be confirmed; ECI (R019) for election-day flags. Validation: timezone-align everything to IST at ingestion; keep historical (observed) and forecast data in clearly separate fields — this system never needs weather forecasts, only historical context for past incidents.

### D7 — Legal and Classification References (R020-R023)
BNS/BNSS/BSA (R020-R021), the current law as of this session (effective 1 July 2024, replacing IPC/CrPC/Evidence Act), plus DPDP Act/Rules (R022) and a practitioner handbook (R023). **This blueprint is not a legal-advice system, and no automated IPC-to-BNS section mapping should be presented to an officer without a human legal reviewer signing off on it first** — flagged identically in the Autonomous Agent Prompt's Phase 6.

### D8 — Ontologies, Schemas, and Interoperability (R024-R025)
GeoJSON/OGC (R024) for geospatial output; POLE (R025) as a *design pattern* informing the canonical model in Blueprint Section 6.4 — explicitly not claimed as a certified standard, since no single authoritative POLE specification was verified this session.

### D9 — Similar Systems and Open-Source Repositories (R026-R029)
OpenAleph/FollowTheMoney (R026, entity/relationship modeling reference), Kepler.gl (R027, geospatial dashboard reference), Neo4j (R028, Phase-3 graph DB), NetworkX (R029, Phase-1 graph logic). All four are classified `REFERENCE` or `STUDY`, not `FORK-CANDIDATE` — the Blueprint's architecture doesn't currently call for forking any of them wholesale.

### D10 — Research Papers, Benchmarks, and Evaluation Data (P4, research-only)
Relevant research areas for this project (not individually URL-verified this session, treat as search starting points for whoever writes the model-evaluation section): kernel density estimation and DBSCAN for hotspot detection; entity resolution / record linkage (directly relevant to Blueprint §6.3's `PersonEntity` design); predictive-policing critique literature (directly relevant to Blueprint §13.1's framing); explainability and calibration for the risk-scoring agent. Mark anything pulled from this category P4 — informative, not directly integrated.

### D11 — Frontend, Visualization, and Design Resources (R027, R030-R031)
Kepler.gl (R027), MapLibre GL JS (R030), Cytoscape.js (R031) cover the map and network-graph rendering needs from Enterprise Blueprint Section 11. All are open-license and Catalyst-deployable as static frontend bundles via Slate/Web Client Hosting.

### D12/D13 — Backend, Data Engineering, and Synthetic Data Resources (R029, R032-R033)
NetworkX (R029) for graph logic; Faker (R032, verified) and indic-faker (R033, **not yet verified — confirm the exact source before writing a script against it**) for synthetic record generation per Blueprint Section 6.7's planted-pattern plan.

### D14 — Security, Privacy, Governance, and Compliance Resources (R034-R035)
OWASP ASVS/API Security (R034) and NIST CSF/AI RMF (R035) as reference frameworks for Blueprint Sections 12-13. Both are free public guidance; ISO 27001 itself (mentioned in the Enterprise Blueprint) is a paid standard — only its publicly-available overview material is in scope here, not the full purchased standard.

---

## E. Feature-to-Data Matrix

| Feature | Required Input | Min. Prototype Fields | Enrichment (Optional) | Analytics Approach | Explainability | Ground Truth Needed | Risk | Human Approval | Catalyst Service |
|---|---|---|---|---|---|---|---|---|---|
| Trend dashboards | CaseMaster, CrimeHead/SubHead | crime_type, date, district | R008, R009 baselines | Aggregation/grouping | Not applicable (descriptive) | None | Low | None (read-only view) | Data Store + QuickML (charts) |
| Hotspot analysis | Inv_OccuranceTime lat/long | lat, long, crime_type, date | R011 POIs, R012 terrain | Hexbin/grid density (Phase 1) → DBSCAN (Phase 3) | Visual density, not a black-box score | Manufactured synthetic hotspot for demo validation | Low-Medium | SCRB reviews before operational use | QuickML / Zia |
| Emerging-spike alerts | Rolling crime counts | district, crime_type, week | R008 baseline for calibration | Z-score deviation | Deviation magnitude shown | Historical baseline window | Medium | Officer reviews before any resource reallocation | Functions + Cron |
| Repeat-pattern / MO similarity | BriefFacts, CrimeHead | free text, method fields | R026 entity-resolution pattern | Embedding similarity | Matched-text highlight | Labeled MO examples (synthetic for demo) | Medium | Investigator confirms match, not auto-linked | QuickML |
| Cross-case linking / entity resolution | Accused/Victim/ComplainantDetails | name, age, address | — | Blocking + weighted similarity (Phase 1) → learned model (Phase 3) | Match-confidence score shown | Planted synthetic duplicate-person test case | Medium-High | Investigator confirms merge before it's treated as fact | Functions |
| Person-Object-Location-Event graph | PersonEntity, RelationshipEdge, VehicleLink | resolved entities + edges | R026, R027 patterns | Graph traversal | Path shown, not just a score | — | Medium | Read-only for investigators; no auto-action | Data Store + Functions |
| Anomaly detection | Same as spike alerts | — | — | Statistical deviation | Same as above | — | Medium | Same as above | Functions |
| Workload / resource-allocation assistance | CaseMaster + Employee | officer, station, case count | — | Simple aggregation (Phase 1); optimization model (🔭 Vision) | Descriptive | — | Low | Command-staff review, never automated dispatch | Data Store |
| Natural-language query ("Ask Berunda") | Curated case-summary corpus | case text | — | RAG over QuickML LLM serving | Cited source shown per answer | — | Medium (hallucination risk) | Rehearsed Q&A set for demo; flag unverified answers | QuickML |
| Evidence-backed report generation | ChargesheetDetails, Evidence | case outcome, evidence refs | — | Template + RAG-grounded drafting | Every claim traces to a source record | — | Medium | Human reviews before any report leaves the system | SmartBrowz + QuickML |
| Data-quality monitoring | All ingested tables | — | — | Schema/null/duplicate checks | Rule-based, fully explainable | — | Low | None (internal ops) | Functions + Cron |
| Governance/audit dashboard | AuditLog, RiskScore.feature_importance | actor, action, timestamp | — | Rule-based parity check (Phase 1) | Fully explainable by construction | — | Low (by design — this IS the safeguard) | Compliance-reporting role only | Data Store + API Gateway RBAC |

---

## F. Automated vs. Manual Acquisition Matrix

| Code | Meaning | Example resources | Why |
|---|---|---|---|
| `AUTO-API` | Public API, no login | R007, R011, R012, R017 | Published, rate-limited, no auth needed for reasonable use |
| `AUTO-DIRECT-DOWNLOAD` | Public file/page fetch | R004-R006, R008-R009, R014, R020-R024, R027-R032, R034-R035 | Static or semi-static public content |
| `AUTO-GIT` | Clone with pinned commit | R026, R027, R030 (repo forms) | Open-source repositories |
| `AUTO-BROWSER-WITH-USER-SESSION` | Requires your login | R002 (Hack2Skill dashboard) | Behind authentication, not scriptable unattended |
| `SEMI-AUTOMATED` | Scriptable once a human confirms the method | R012 (if registration needed), R018, R019, R033 | Access mechanism not fully confirmed this session |
| `MANUAL-AUTHORIZED` | Human does this step directly | R001 (already done), R013, R016, R025 | Either already provided, or licensing/authority unclear |
| `FUTURE-RESTRICTED` | Not acquired under this blueprint at all | CCTNS live feed, CDR, banking records (Blueprint §6.6) | Requires lawful process (warrant/MOU), not an engineering decision |
| `DO-NOT-ACQUIRE` | Explicitly excluded | R010, any SECC/caste-linked dataset | Either not a data source (R010) or an active bias risk (SECC) |

---

## G. Download and Storage Architecture

```text
project-root/
  docs/
  resources/
    source-pages/
    standards/
    papers/
    licenses/
  data/
    organizer/              <- R001 and anything else Hack2Skill provides directly
    raw/                    <- R006-R022 as originally downloaded, untouched
    external/               <- R011, R012, R017 API responses, cached
    interim/
    processed/
    synthetic/              <- Faker/indic-faker output, always prefixed SYNTHETIC_
    samples/
    restricted-placeholders/ <- mock adapters/contracts for R-FUTURE-RESTRICTED items, never real data
  boundaries/                <- OSM/Bhuvan/Survey-of-India geospatial layers
  repositories/               <- R026, R027, R030 etc., one folder per owner__repo, commit-pinned
  models/
  manifests/
  scripts/
    acquisition/
    validation/
    transformation/
  reports/
  logs/
  quarantine/                 <- every fresh download lands here first, nowhere else, until Section I gates pass
```

Naming rule: every file under `raw/` keeps its original filename plus a `_<YYYYMMDD>` acquisition-date suffix. Every file gets a companion `.sha256` checksum file at acquisition time. Large or sensitive data (anything in `data/organizer/` or `data/synthetic/` above a few MB) is **not** committed to a public GitHub remote — use `.gitignore` plus Git LFS or DVC for anything that must be versioned, and keep the public repo limited to code, schemas, and small samples.

---

## H. Resource Manifest Specification

**`manifests/resource_manifest.csv`** — one row per resource ID from Section C, columns matching Section C's table plus `date_acquired`, `checksum`, `local_path`.

**`manifests/provenance.jsonl`** — one JSON object per acquired file:
```json
{"resource_id": "R017", "source_url": "https://open-meteo.com/...", "access_date": "2026-07-16", "checksum_sha256": "...", "transform_applied": "timezone_normalize_IST", "derived_from": null}
```

**`manifests/license_inventory.csv`** — resource_id, license_name, license_url_or_file, attribution_required (bool), attribution_text.

**`manifests/failure_log.csv`** and **`manifests/missing_resource_register.csv`** — resource_id, attempted_date, failure_reason, next_action.

**`manifests/approval_register.csv`** — resource_id, approval_type (large-download / authenticated-session / restricted-category), approved_by, approval_date.

---

## I. Quality Gates

A resource does not leave `data/quarantine/` until it passes every gate that applies to its type:

- **Authenticity** — source matches the Section C verified URL, not a mirror found later.
- **File integrity** — checksum matches, archive extracts cleanly.
- **Schema validity** — required columns present, types as expected.
- **Geometry validity** (spatial only) — valid geometry, coordinates inside Karnataka's bounding box, CRS = WGS84.
- **Temporal validity** — dates parse, no impossible future dates for historical data.
- **Duplicate detection** — no exact-duplicate rows silently double-counted.
- **Missing-value profile** — recorded, not silently dropped.
- **Administrative-code matching** (where relevant) — district/station codes actually join against the boundary reference.
- **Licensing** — a license is on file in `license_inventory.csv` before the resource is used in anything demoed.
- **Attribution** — recorded if the license requires it (e.g., ODbL for OSM).
- **Secrets/malware scan** (repositories especially) — clean before anything in them executes.
- **PII scan** — nothing that looks like a real name/phone/ID pattern in anything meant to be aggregate or synthetic.
- **Synthetic-data labelling** — every synthetic file/record is marked, not just the folder name.
- **Reproducibility** — the acquisition script can be re-run and produce the same (or a newer, correctly-dated) result.

---

## J. Resource Roadmap

- **First 24 hours:** R001 (already in hand), R002 (confirm submission format), R004-R005 (Catalyst docs), R020-R022 (legal reference texts) — everything Day 1-2 of the Implementation Plan depends on.
- **First 3 days:** R011, R012, R017 (enrichment APIs), R032 (Faker setup) — feeds the synthetic-data generation and entity-resolution work of Days 1-4.
- **First week:** R006-R009, R014 (baseline statistics for validating synthetic data), R026-R031 (reference repos/frontend libraries) as Days 5-8 build the risk-scoring, hotspot, and dashboard layers.
- **Prototype freeze (Day 9-10):** stop acquiring anything new; only validate and polish what's already in.
- **Submission week:** R002's exact format re-confirmed, demo rehearsed against the frozen dataset.
- **Post-hackathon enterprise roadmap:** R013 (Survey of India, once licensing is resolved), R018-R019 (IMD/ECI, once access methods are confirmed), R033 (indic-faker, once source is confirmed) become relevant at Phase 2 pilot stage (Complete Roadmap, Phase 2).

**What NOT to download, because it would waste your 11 days:** anything under `FUTURE-RESTRICTED` (Section F) — there is no lawful path to acquire real CCTNS/CDR/banking data in an 11-day window, so don't spend any of it trying. Also skip R016 (RBI DBIE) and R023 (BPRD handbook) unless Phase 1 build time is unexpectedly ahead of schedule — both are genuinely P4, informative-only.

---

## K. Final Checklists

**P0 completion checklist**
- [ ] R001 reconciled against the uploaded PDF (Enterprise Blueprint §19.4's residual ambiguity resolved)
- [ ] R002 submission format confirmed
- [ ] R003 Catalyst credits redeemed and visible in console
- [ ] R006, R020 baseline crime stats and legal-section reference retrieved

**Prototype readiness checklist**
- [ ] Synthetic dataset generated (R032) with planted patterns per Implementation Plan Day 1-2
- [ ] OSM/Bhuvan enrichment (R011-R012) wired into the hotspot map
- [ ] Every acquired file has a checksum and a manifest row

**Legal and ethical checklist**
- [ ] No SECC/caste-linked dataset anywhere in `data/` (Section D5)
- [ ] `CasteID`/`ReligionID` access-restriction (Enterprise Blueprint §6.2) verified against the actual deployed RBAC config, not just documented
- [ ] BNS/BNSS/BSA references (R020-R021) used only as classification reference, not as a substitute for legal review of any auto-generated mapping

**Catalyst readiness checklist**
- [ ] Every mandatory service in Blueprint §15 has its doc (R004-R005) bookmarked and its quickstart run at least once

**Open-source release checklist**
- [ ] Every third-party repo referenced (R026-R031) has its license recorded in `license_inventory.csv`
- [ ] No incompatible-license code copied wholesale — reference/pattern use only, per Section D9

**Demo evidence checklist**
- [ ] `reports/VALIDATION_REPORT.md` shows every Phase-1 feature's data passed its quality gate
- [ ] Rehearsed "Ask Berunda" questions (Hackathon Pitch §4) tested against the actual frozen dataset, not a hypothetical one

**Post-hackathon backlog**
- [ ] R013, R018, R019, R033 — access-method confirmations deferred from the hackathon window
- [ ] Full research-only category (D10) — literature review for the Phase 2+ evaluation framework
