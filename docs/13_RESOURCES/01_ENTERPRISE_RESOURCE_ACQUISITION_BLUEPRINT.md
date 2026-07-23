# Enterprise Resource Acquisition Blueprint

[//]: # (Document ID: BERUNDA-RSRC-BP-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: Project Berunda master prompt, blueprints/h2s/Project_Berunda_06_Resource_Acquisition_Blueprint.md | Last Verified: 2026-07-18 | Review: Weekly)

---

## A. Executive Resource Strategy

**Purpose:** Identify, classify, and prescribe the acquisition of every resource — datasets, documents, SDKs, repositories, standards, and research — that Project Berunda requires to build a lawful, explainable, privacy-preserving, production-viable crime-intelligence platform, from hackathon prototype through enterprise deployment.

**Hackathon objective vs. enterprise objective:** The hackathon objective is a working, demoable prototype built on organizer-provided schemas, lawfully public data, and clearly labelled synthetic records. The enterprise objective — real CCTNS integration, cross-district/cross-state correlation, and operational deployment — depends on data-sharing agreements and legal review that are out of scope for unattended acquisition. This blueprint distinguishes both.

**Prototype data boundary:** No resource acquired under this blueprint may include real victim, witness, accused, biometric, banking, telecom, Aadhaar, private-message, or precise-residential data. Restricted categories are represented only through clearly labelled synthetic records (D13) or documented future-integration contracts (P3).

**Data classification:**

| Class | Meaning | Examples |
|-------|---------|---------|
| Authorized | Provided directly by the Datathon organizers | ERD, data dictionary, sample data |
| Public | Lawfully public, appropriately licensed government or open data | NCRB reports, OSM, Census aggregates |
| Synthetic | Generated, clearly labelled, never presented as real | Faker/indic-faker output |
| Restricted | Real systems represented only as future integration contracts | CCTNS live feed, telecom CDR, banking records |

**Resource-acquisition principles:**

1. **Data minimization** — acquire only what a specific, named feature needs
2. **Privacy by design** — restricted/sensitive fields excluded from acquisition scope entirely, not collected-then-restricted
3. **Security by design** — every download lands in quarantine before validation; nothing trusted by default
4. **Open-source compliance** — no code or data treated as reusable without a clear, checked license
5. **Reproducibility** — every acquisition logged with source, date, and checksum; repeatable identically
6. **Provenance / chain of custody** — every dataset's origin, access date, and transformation history tracked in manifests
7. **Human approval points** — authenticated access, large downloads, or restricted-category data require named human sign-off

**Definitions:**

| Term | Meaning |
|------|---------|
| Downloaded | File exists on disk with recorded checksum and source URL |
| Verified | Passed Section I quality gates relevant to its type |
| Usable | Verified, and schema mapped to at least one feature in Section E |
| Production-approved | Usable, and passed a named human's sign-off for its declared classification |

---

## B. Priority Levels

| Priority | Meaning | Examples |
|----------|---------|---------|
| P0 — Competition-critical | Organizer material; missing blocks submission | ERD, rules, Catalyst credits, submission format |
| P1 — Prototype-critical | Required to implement and demo the core platform | Catalyst SDKs, geospatial data, synthetic-data tooling |
| P2 — Enterprise-enrichment | Improves accuracy, scalability, governance, or presentation | NCRB statistics, socio-economic context, reference repos |
| P3 — Future authorized integrations | Restricted systems represented only as interface contracts — never acquired as real data | CCTNS, CDR, banking records |
| P4 — Research-only | Papers, benchmarks, reference implementations for design decisions | KDE surveys, entity-resolution literature, predictive-policing critique |

---

## C. Master Resource Inventory

Each row uses the following 32-column schema. Columns are abbreviated in the table where context is clear.

**Column key:**
1. RSRC ID · 2. Priority · 3. Category · 4. Resource name · 5. Why needed · 6. Feature enabled · 7. Preferred source · 8. Verified landing URL · 9. Backup source · 10. Publisher · 11. Geo coverage · 12. Temporal coverage · 13. Granularity · 14. Format · 15. Expected size · 16. Update frequency · 17. License/terms · 18. Attribution required · 19. Personal-data risk · 20. Legal-access class · 21. Auto-acquisition feasibility · 22. Recommended method · 23. Auth required · 24. Human approval · 25. Rate limits · 26. Validation procedure · 27. Storage path · 28. Data owner · 29. Retention · 30. Catalyst mapping · 31. Known limitation · 32. Acceptance criterion

Where a cell is empty the field is not applicable to that resource type.

### D1 — Official Datathon Material

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Backup | Publisher | Geo | Temp | Gran | Fmt | Size | Freq | License | Attr | PII | Legal | Auto | Method | Auth | Approve | Limits | Validate | Path | Owner | Retain | Catalyst | Limit | Accept |
|------|-----|-----|----------|-----|---------|--------|-----|--------|-----------|-----|------|------|-----|------|------|---------|------|-----|-------|------|--------|------|---------|--------|----------|------|-------|--------|----------|--------|--------|
| RSRC-001 | P0 | D1 | Challenge rules & timeline | Defines submission requirements | All features | Hack2Skill dashboard | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill | India | 2026 | — | HTML/PDF | <1 MB | Static | Organizer terms | No | None | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Confirm exact submission format | `data/organizer/` | Both | Indefinite | — | Login-gated | Submission format confirmed |
| RSRC-002 | P0 | D1 | ERD / Database Design Document | Canonical schema for Data Store tables | All data features | Hack2Skill Resources tab | Already in hand as `Police_FIR_ER_Diagram.pdf` | — | Hack2Skill/KSP | Karnataka | 2026 | Table/field | PDF | ~2 MB | Static | Organizer terms | No | Medium (schema design) | Authorized | No | MANUAL-AUTHORIZED | — | Done | — | Match uploaded PDF exactly | `data/organizer/` | Both | Indefinite | Data Store | Already acquired | Matches uploaded PDF byte-for-byte |
| RSRC-003 | P0 | D1 | Data dictionary | Field-level semantics for synthetic generation | All data features | Hack2Skill Resources tab | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill/KSP | Karnataka | 2026 | Field | PDF/CSV | <5 MB | Static | Organizer terms | No | None | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Parse; confirm columns match ERD | `data/organizer/` | Both | Indefinite | Data Store | May not exist as separate file | All ERD fields documented |
| RSRC-004 | P0 | D1 | Sample data records | Realistic seed for synthetic generation | Synthetic data | Hack2Skill Resources tab | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill/KSP | Karnataka | 2026 | Record-level | CSV/JSON | <10 MB | Static | Organizer terms | Yes | Medium (sample data) | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Schema validation, anonymization check | `data/organizer/` | Both | Indefinite | Data Store | May contain real anonymized test data | Parses; schema matches ERD |
| RSRC-005 | P0 | D1 | Submission requirements & judging rubric | Defines demo evidence needed | Demo/pitch | Hack2Skill dashboard | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill | India | 2026 | — | HTML/PDF | <1 MB | Static | Organizer terms | No | None | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Confirm before Day 10 | `data/organizer/` | Both | Indefinite | — | Must be confirmed | Rubric acquired and mapped to features |
| RSRC-006 | P0 | D1 | Catalyst credit redemption instructions | Needed to deploy on Catalyst | All Catalyst features | Catalyst promotions page | `catalyst.zoho.com/promotions.html?cn=KSPH26` | — | Hack2Skill/Zoho | Global | 2026 | — | HTML | <1 MB | Static | Promo terms | No | None | Authorized | Yes | AUTO-DIRECT-DOWNLOAD | No | No | — | Credits visible in console | `data/organizer/` | Both | Until credits expire | All | Time-limited code | Credits redeemable |
| RSRC-007 | P0 | D1 | FAQs & announcements | Clarifies ambiguous requirements | All | Hack2Skill dashboard | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill | India | 2026 | — | HTML | <1 MB | Per-event | Organizer terms | No | None | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Human review for relevance | `data/organizer/` | Both | Indefinite | — | Event-driven | All FAQs reviewed before Day 3 |
| RSRC-008 | P0 | D1 | Required presentation/video format | Defines final deliverable structure | Submission | Hack2Skill dashboard | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Hack2Skill | India | 2026 | — | HTML/PDF | <1 MB | Static | Organizer terms | No | None | Authorized | No | AUTO-BROWSER-WITH-USER-SESSION | Yes | Yes | — | Confirm format and duration | `data/organizer/` | Both | Indefinite | — | Changes may occur | Format confirmed before Day 10 |

### D2 — Zoho Catalyst Platform Resources

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | Geo | Temp | Fmt | License | PII | Legal | Auto | Method | Auth | Approve | Validate | Path | Catalyst | Limit |
|------|-----|-----|----------|-----|---------|--------|-----|--------|-----|------|-----|---------|-----|-------|------|--------|------|---------|----------|------|----------|--------|
| RSRC-009 | P1 | D2 | Catalyst Functions docs | Serverless backend logic | All backend | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Quickstart runs | `resources/source-pages/` | Functions | Docs evolve |
| RSRC-010 | P1 | D2 | Catalyst AppSail docs | Custom/manged runtime hosting | Backend services | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Quickstart runs | `resources/source-pages/` | AppSail | Docs evolve |
| RSRC-011 | P1 | D2 | Catalyst Data Store docs | MySQL-compatible relational DB | All data persistence | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Schema creates | `resources/source-pages/` | Data Store | Docs evolve |
| RSRC-012 | P1 | D2 | Catalyst QuickML docs | ML model serving, RAG, AutoML | AI/ML features | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Sample model deploys | `resources/source-pages/` | QuickML | Docs evolve |
| RSRC-013 | P1 | D2 | Catalyst Zia Services docs | OCR, face, text, barcode | Document analysis | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | API returns valid result | `resources/source-pages/` | Zia Services | Docs evolve |
| RSRC-014 | P1 | D2 | Catalyst SmartBrowz docs | PDF/report generation | Evidence-backed reports | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Template renders PDF | `resources/source-pages/` | SmartBrowz | Docs evolve |
| RSRC-015 | P1 | D2 | Catalyst Signals docs | Event-driven messaging | Notifications, triggers | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Event fires and is received | `resources/source-pages/` | Signals | Docs evolve |
| RSRC-016 | P1 | D2 | Catalyst Circuits docs | Workflow orchestration | Multi-step processes | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Workflow executes test | `resources/source-pages/` | Circuits | Docs evolve |
| RSRC-017 | P1 | D2 | Catalyst API Gateway docs | Auth, rate limiting, routing | All API endpoints | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Route configured and tested | `resources/source-pages/` | API Gateway | Docs evolve |
| RSRC-018 | P1 | D2 | Catalyst Cache docs | In-memory caching | Performance | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Cache hit/miss works | `resources/source-pages/` | Cache | Docs evolve |
| RSRC-019 | P1 | D2 | Catalyst Cron/Job Scheduler docs | Scheduled tasks | Data refresh, alerts | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Cron job triggers function | `resources/source-pages/` | Cron | Docs evolve |
| RSRC-020 | P1 | D2 | Catalyst Stratus docs | Distributed event processing | Real-time analytics | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Event processes through Stratus | `resources/source-pages/` | Stratus | Docs evolve |
| RSRC-021 | P1 | D2 | Catalyst NoSQL docs | Document store | Flexible schema data | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | CRUD operations work | `resources/source-pages/` | NoSQL | Docs evolve |
| RSRC-022 | P1 | D2 | Catalyst IAM & RBAC docs | Access control | Security | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Role-based access enforced | `resources/source-pages/` | IAM | Docs evolve |
| RSRC-023 | P1 | D2 | Catalyst CLI & Local Dev docs | Local development | All features | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | HTML | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | CLI installs and authenticates | `resources/source-pages/` | All | Docs evolve |
| RSRC-024 | P2 | D2 | Catalyst Circuits workflow templates | Reference workflow patterns | Workflow orchestration | Zoho help | `help.catalyst.zoho.com` | Zoho | Global | Current | Code | Zoho ToS | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | No | No | Templates load into console | `resources/source-pages/` | Circuits | May be limited |

#### Feature-to-Catalyst-Service Mapping

| Feature Layer | Catalyst Service | Role |
|--------------|-----------------|------|
| Frontend hosting | Slate / Web Client Hosting | SPA deployment |
| Authentication | API Gateway + IAM | RBAC, session management |
| REST API backend | Functions | All business logic endpoints |
| Relational persistence | Data Store | CaseMaster, PersonEntity, ChargesheetDetails |
| Document/flexible storage | NoSQL | Evidence metadata, unstructured notes |
| Caching | Cache | Session state, frequent queries |
| ML model serving | QuickML | Embedding, RAG, AutoML |
| AI vision/OCR | Zia Services | Document analysis |
| PDF/report generation | SmartBrowz | Evidence-backed reports |
| Event-driven messaging | Signals | Async notifications, data-change events |
| Workflow orchestration | Circuits | Multi-step investigation workflows |
| Scheduled tasks | Cron | Data refresh, periodic analysis |
| Real-time event processing | Stratus | Streaming analytics |
| Async processing | AppSail | Long-running computation |
| Email notifications | Mail | Alerts, report delivery |
| Push notifications | Push Notifications | Mobile alerts |
| Logging & monitoring | Catalyst Console Logs | Observability |
| Secrets management | Catalyst Connections/Environment Variables | API keys, credentials |
| Environment separation | Catalyst Projects + Deploy | Dev/staging/prod |

**Areas requiring custom open-source components hosted through Catalyst:** Graph visualization (Cytoscape.js), map rendering (MapLibre GL JS), heavy geospatial processing (Python with Shapely/GeoPandas via Functions), and synthetic data generation (Faker via local script, not real-time).

### D3 — Crime and Public-Safety Statistics

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Backup | Publisher | Geo | Temp | Gran | Fmt | Size | Freq | License | Attr | PII | Legal | Auto | Method | Validate | Path | Limit |
|------|-----|-----|----------|-----|---------|--------|-----|--------|-----------|-----|------|------|-----|------|------|---------|------|-----|-------|------|--------|----------|------|--------|
| RSRC-025 | P0 | D3 | NCRB Crime in India 2022 (full report) | National baseline for validation | Trend dashboards, validation | ncrb.gov.in | `ncrb.gov.in` | data.gov.in | NCRB (MHA) | India | 2022 | District | PDF | ~50 MB | Annual | Govt publication | Yes | None (aggregate) | Public | Yes | AUTO-DIRECT-DOWNLOAD | File integrity, parse district tables | `data/raw/ncrb/` | Latest report may be 2022 |
| RSRC-026 | P2 | D3 | NCRB Crime in India machine-readable tables | Automated baseline comparison | Trend dashboards | data.gov.in | `data.gov.in/ministrydepartment/National%20Crime%20Records%20Bureau%20(NCRB)` | — | NCRB/data.gov.in | India | 2001-2022 | District | CSV/API | ~100 MB | Annual | GODL-India | Yes | None | Public | Yes | AUTO-API | Parse CSV, validate district codes | `data/raw/ncrb/` | Coverage varies by dataset |
| RSRC-027 | P1 | D3 | Karnataka Crime Review (monthly/yearly) | State-level baseline for validation | Karnataka features | ksp.karnataka.gov.in | `ksp.karnataka.gov.in/new-page/Monthly%20Crime%20Review/en` | — | Karnataka State Police | Karnataka | 2024-2026 | District | PDF | ~10 MB/month | Monthly | Govt of Karnataka ToS | Yes | None (aggregate) | Public | Yes | AUTO-DIRECT-DOWNLOAD | Parse, confirm district coverage | `data/raw/ksp/` | Page structure may change |
| RSRC-028 | P2 | D3 | Karnataka crime data on OGD Platform | Machine-readable state crime data | Trend analysis | data.gov.in | `karnataka.data.gov.in/catalog/crime-review-year-2023` | — | KSP/Data.gov.in | Karnataka | 2023-2025 | District | CSV | ~20 MB | Annual | GODL-India | Yes | None | Public | Yes | AUTO-API | Parse CSV | `data/raw/ksp/` | Coverage varies |
| RSRC-029 | P2 | D3 | NITI Aayog NDAP crime statistics | Cross-sectoral crime indicators | Sociological correlation | ndap.niti.gov.in | `ndap.niti.gov.in` | — | NITI Aayog | India | Varies | State/district | CSV | ~50 MB | Periodic | NDAP open terms | Yes | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | Column match listing | `data/raw/ndap/` | Not always district-level |

### D4 — Administrative and Geospatial Data

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | Geo | Format | License | Attr | PII | Legal | Auto | Method | Validate | Path | Limit |
|------|-----|-----|----------|-----|---------|--------|-----|-----------|-----|--------|---------|------|-----|-------|------|--------|----------|------|--------|
| RSRC-030 | P1 | D4 | OpenStreetMap Karnataka points of interest | Location enrichment: police stations, hospitals, schools, ATMs | Hotspot analysis, geospatial context | Overpass API | `overpass-api.de` | OSM Foundation | Karnataka | JSON/GeoJSON | ODbL | Yes | None | Public | Yes | AUTO-API | Geometry validity, coordinate bounds | `data/external/osm/` | Rural coverage may be sparse |
| RSRC-031 | P1 | D4 | Bhuvan thematic WMS/WFS layers | Terrain, LULC, water bodies, satellite imagery | Geospatial context, map layers | Bhuvan (ISRO/NRSC) | `bhuvan.nrsc.gov.in` | ISRO/NRSC | India | WMS/WFS/GeoTIFF | Indian govt freeware | Yes | None | Public | Yes | AUTO-API (WMS/WFS) | WMS layer renders in test map | `boundaries/bhuvan/` | May need registration |
| RSRC-032 | P2 | D4 | Karnataka administrative boundaries (districts, taluks) | Mapping crime to admin units | All geospatial features | Survey of India / data.gov.in | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Survey of India | Karnataka | SHP/GeoJSON | `UNVERIFIED` | — | None | Public (TBC) | No | MANUAL-AUTHORIZED | Geometry validity, CRS, admin code join | `boundaries/karnataka/` | Some SOI products not freely licensed |
| RSRC-033 | P2 | D4 | Karnataka police jurisdiction boundaries | Police station boundaries | Station drill-down, patrol planning | Karnataka Police / data.gov.in | `UNVERIFIED — REQUIRES HUMAN CHECK` | — | Karnataka Police | Karnataka | SHP/GeoJSON | `UNVERIFIED` | — | None | Public (TBC) | No | SEMI-AUTOMATED | Geometry validity, topology | `boundaries/karnataka/` | Not publicly available in all states |
| RSRC-034 | P2 | D4 | OpenStreetMap road/railway network | Transport infrastructure context | Correlation analysis | Overpass API | `overpass-api.de` | OSM Foundation | Karnataka | JSON/GeoJSON | ODbL | Yes | None | Public | Yes | AUTO-API | Geometry validity | `data/external/osm/` | Large query may hit rate limits |
| RSRC-035 | P2 | D4 | Bhuvan CartoDEM (30m) | Elevation data for geospatial analysis | Terrain context | Bhuvan (ISRO/NRSC) | `bhuvan.nrsc.gov.in` | ISRO/NRSC | India | GeoTIFF | Indian govt freeware | Yes | None | Public | Yes | AUTO-DIRECT-DOWNLOAD | Valid raster, CRS check | `boundaries/dem/` | ~1 GB for full Karnataka |

**Coordinate system standard:** All spatial data normalized to WGS84 (EPSG:4326) at ingestion. Administrative codes must match the project's canonical Karnataka code table.

### D5 — Census, Socio-Economic, and Development Indicators

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | Geo | Temp | Gran | Fmt | License | Attr | PII | Legal | Auto | Method | Validate | Path | Limit |
|------|-----|-----|----------|-----|---------|--------|-----|-----------|-----|------|------|-----|---------|------|-----|-------|------|--------|----------|------|--------|
| RSRC-036 | P2 | D5 | Census of India 2011 District Census Handbook (Karnataka) | Population, density, urban/rural, literacy aggregates | Socio-economic correlation | censusindia.gov.in | `censusindia.gov.in` | Registrar General | Karnataka | 2011 | District | PDF/CSV | Govt publication | Yes | None (aggregate) | Public | Yes | AUTO-DIRECT-DOWNLOAD | Parse, confirm district coverage | `data/raw/census/` | 2021 Census postponed; 2011 is latest full |
| RSRC-037 | P2 | D5 | NITI Aayog NDAP socio-economic indicators | Cross-sectoral development indicators | Correlation analysis | ndap.niti.gov.in | `ndap.niti.gov.in` | NITI Aayog | India | Varies | District | CSV | NDAP open terms | Yes | None (aggregate) | Public | Yes | AUTO-DIRECT-DOWNLOAD | Column match listing | `data/raw/ndap/` | Coverage varies by indicator |
| RSRC-038 | P4 | D5 | RBI DBIE macro/financial indicators | Optional macro context | Research-only | rbi.org.in | `UNVERIFIED — REQUIRES HUMAN CHECK` | RBI | India | Varies | State | CSV | RBI terms | — | None | Public | No | MANUAL-AUTHORIZED | — | `data/raw/rbi/` | Not needed for Phase 1 |

**Explicit prohibition:** Caste, religion, ethnicity, disability, or other protected characteristics must not be used as predictive enforcement features. Such information may only be used, where lawful, for aggregated fairness auditing.

### D6 — Weather, Environment, and Temporal Context

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | Geo | Temp | Gran | Fmt | License | Auto | Method | Validate | Path |
|------|-----|-----|----------|-----|---------|--------|-----|-----------|-----|------|------|-----|---------|------|--------|----------|------|
| RSRC-039 | P1 | D6 | Open-Meteo historical weather API | Weather correlation for crime patterns | Emerging-spike alerts | open-meteo.com | `open-meteo.com` | Open-Meteo | Karnataka | Historical + forecast | Hourly/daily | JSON | Free/open (check volume terms) | Yes | AUTO-API | Date range, null counts, IST timezone | `data/external/weather/` |
| RSRC-040 | P2 | D6 | IMD official weather data | Official backup/validation | Weather features | mausam.imd.gov.in | `mausam.imd.gov.in` | IMD | India | Historical | Daily | `UNVERIFIED` | Govt terms | No | SEMI-AUTOMATED | Access method TBD | `data/external/weather/` |
| RSRC-041 | P2 | D6 | Indian public holidays & festivals calendar | Temporal context for crime patterns | Trend analysis | indiacode.nic.in / government portal | `UNVERIFIED — REQUIRES HUMAN CHECK` | Govt of India | India | 2024-2026 | Daily | CSV/JSON | Govt publication | Yes | AUTO-DIRECT-DOWNLOAD | Date validation, coverage | `data/external/temporal/` |
| RSRC-042 | P2 | D6 | Karnataka election dates (ECI) | Election-day flags for temporal features | Correlation analysis | eci.gov.in | `eci.gov.in` | ECI | Karnataka | 2018-2026 | Event | HTML/PDF | Govt terms | Yes | SEMI-AUTOMATED | Verify against known election dates | `data/external/temporal/` |

**Temporal alignment:** All datetime data normalized to IST (UTC+5:30). Historical and forecast data kept in clearly separate fields. Missing values recorded, not silently dropped.

### D7 — Legal and Classification References

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | Fmt | License | Auto | Method | Validate | Path |
|------|-----|-----|----------|-----|---------|--------|-----|-----------|-----|---------|------|--------|----------|------|
| RSRC-043 | P0 | D7 | Bharatiya Nyaya Sanhita (BNS) 2023 — official text | Maps to real IPC/BNS Sections field | Crime-category mapping | indiacode.nic.in | `indiacode.nic.in` | MHA / India Code | PDF | Public domain | Yes | AUTO-DIRECT-DOWNLOAD | Cross-check sections against sample FIR data | `resources/standards/legal/` |
| RSRC-044 | P1 | D7 | Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 | Companion procedural law | Legal reference | indiacode.nic.in | `indiacode.nic.in` | MHA / India Code | PDF | Public domain | Yes | AUTO-DIRECT-DOWNLOAD | Retrieved | `resources/standards/legal/` |
| RSRC-045 | P1 | D7 | Bharatiya Sakshya Adhiniyam (BSA) 2023 | Companion evidence law | Legal reference | indiacode.nic.in | `indiacode.nic.in` | MHA / India Code | PDF | Public domain | Yes | AUTO-DIRECT-DOWNLOAD | Retrieved | `resources/standards/legal/` |
| RSRC-046 | P1 | D7 | DPDP Act 2023 & DPDP Rules 2025 | Compliance framing | Privacy/Governance | meity.gov.in | `meity.gov.in` | MeitY | PDF | Public domain | Yes | AUTO-DIRECT-DOWNLOAD | Retrieved, key sections reviewed | `resources/standards/legal/` |
| RSRC-047 | P2 | D7 | IPC-to-BNS section mapping reference | Legacy data compatibility | Crime-category mapping | bprd.nic.in | `bprd.nic.in` | BPRD, MHA | PDF | Govt publication | Yes | AUTO-DIRECT-DOWNLOAD | Cross-check with BNS text | `resources/standards/legal/` |
| RSRC-048 | P4 | D7 | BPRD BNS practitioner handbook | Practitioner-level guidance | Legal reference | bprd.nic.in | `bprd.nic.in` | BPRD, MHA | PDF | Govt publication | Yes | AUTO-DIRECT-DOWNLOAD | — | `resources/standards/legal/` |

**Notice:** This product is not a legal-advice system. BNS/BNSS/BSA references are used only as classification references. No automated IPC-to-BNS mapping is presented to an officer without a human legal reviewer signing off.

### D8 — Ontologies, Schemas, and Interoperability

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | Publisher | License | Auto | Method | Path |
|------|-----|-----|----------|-----|---------|--------|-----|-----------|---------|------|--------|------|
| RSRC-049 | P4 | D8 | GeoJSON specification (RFC 7946) | Geospatial output format | All geospatial | IETF | `tools.ietf.org/html/rfc7946` | IETF | Open standard | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-050 | P4 | D8 | OGC WMS/WFS/WMTS standards | Map service interoperability | Map layers | OGC | `ogc.org/standards` | OGC | Open standard | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-051 | P4 | D8 | PROV-O provenance ontology | Data lineage standard | Data governance | W3C | `w3.org/TR/prov-o/` | W3C | W3C document license | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-052 | P4 | D8 | Model Cards for Model Reporting (Google) | Model documentation | AI governance | arXiv | `arxiv.org/abs/1810.03993` | Google | CC-BY | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-053 | P4 | D8 | Datasheets for Datasets (Gebru et al.) | Dataset documentation | Data governance | arXiv | `arxiv.org/abs/1803.09010` | Microsoft Research | CC-BY | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-054 | P4 | D8 | POLE (Person-Object-Location-Event) design pattern references | Informs canonical data model | Graph/Link analysis | Policing informatics literature | — | Various | Varies | No | MANUAL-AUTHORIZED | `resources/papers/` |

**Recommended practical canonical crime-data model:** A normalized relational model with CorePerson, CoreCase, CoreIncident, CoreEvidence, CoreLocation, and CoreRelationships tables, with a POLE-style graph view built at query time rather than stored redundantly.

### D9 — Similar Systems and Open-Source Repositories

| RSRC | Pri | Cat | Resource | Why | Source | URL | Maintainer | Last activity | License | Stack | Stars | Reusable module | Architecture idea | Security concern | Maintenance concern | Code allowed | Attr | Classification |
|------|-----|-----|----------|-----|--------|-----|------------|-------------|---------|-------|-------|----------------|-----------------|----------------|-------------------|-------------|------|---------------|
| RSRC-055 | P1 | D9 | OpenAleph / FollowTheMoney | Entity/relationship design reference | github.com | `github.com/alephdata/aleph` | OCCRP | Active | MIT | Python | >1K | Entity resolution patterns | Cross-referencing architecture | Data hosted by user | Active community | Study patterns | Yes | STUDY |
| RSRC-056 | P1 | D9 | Kepler.gl | Geospatial dashboard reference | github.com | `github.com/keplergl/kepler.gl` | Uber/OpenJS | Active | MIT | JavaScript/React | >11K | Hexbin density, heatmap | Filter-driven exploration | Client-side only | Large bundle | Study patterns | Yes | REFERENCE |
| RSRC-057 | P2 | D9 | Neo4j Community Edition | Phase-3 graph DB upgrade path | neo4j.com | `neo4j.com` | Neo4j Inc. | Active | GPLv3 | Java | >11K | Cypher query language | Graph-native storage | Not Catalyst-hosted | Community scale limits | Study patterns | Yes | REFERENCE |
| RSRC-058 | P2 | D9 | NetworkX | Phase-1 graph traversal logic | networkx.org | `github.com/networkx/networkx` | NetworkX devs | Active | BSD | Python | >14K | Graph algorithms | Pure-Python graph | Performance at scale | Fine at prototype scale | pip install | Yes | INTEGRATE |
| RSRC-059 | P2 | D9 | GraphRAG (Microsoft) | Graph-enhanced RAG pattern | github.com | `github.com/microsoft/graphrag` | Microsoft | Active | MIT | Python | >10K | Graph+vector retrieval | Graph-based grounding | Complex setup | Rapidly evolving | Study patterns | Yes | STUDY |
| RSRC-060 | P3 | D9 | CCTNS reference architecture | National crime reporting system patterns | ncrb.gov.in | `ncrb.gov.in` | NCRB/MHA | — | Govt publication | — | — | Integration patterns | National-level architecture | Restricted data | Govt system | Future only | — | FUTURE-RESTRICTED |
| RSRC-061 | P4 | D9 | Predictive policing critique papers | Ethical and methodological limitations | Various | — | Various | — | Varies | — | — | — | Limitations framing | — | — | Study only | Yes | RESEARCH-ONLY |

### D10 — Research Papers, Benchmarks, and Evaluation Data

| RSRC | Pri | Category | Topic | Why | Source | Auto | Method | Path |
|------|-----|----------|-------|-----|--------|------|--------|------|
| RSRC-062 | P4 | D10 | Kernel density estimation for crime hotspots | Hotspot detection reference | arXiv / academic | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |
| RSRC-063 | P4 | D10 | DBSCAN/HDBSCAN for spatiotemporal clustering | Cluster detection reference | arXiv / academic | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |
| RSRC-064 | P4 | D10 | Entity resolution / record linkage surveys | Cross-case linking reference | arXiv / academic | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |
| RSRC-065 | P4 | D10 | Explainable AI (XAI) for public-sector systems | Explainability patterns | arXiv / academic | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |
| RSRC-066 | P4 | D10 | Predictive policing critique and limitations | Ethical framing | Academic / civil society | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |
| RSRC-067 | P4 | D10 | NIST AI Risk Management Framework | AI governance reference | NIST | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/` |
| RSRC-068 | P4 | D10 | Public-sector AI governance guidelines | Governance patterns | Government / OECD | Yes | AUTO-DIRECT-DOWNLOAD | `resources/papers/` |

### D11 — Frontend, Visualization, and Design Resources

| RSRC | Pri | Cat | Resource | Why | Source | URL | License | Bundle | Auto | Method | Path |
|------|-----|-----|----------|-----|--------|-----|---------|--------|------|--------|------|
| RSRC-069 | P2 | D11 | MapLibre GL JS | Open-source interactive maps | github.com | `github.com/maplibre/maplibre-gl-js` | BSD-3-Clause | ~500 KB gzip | Yes | AUTO-GIT / npm | `repositories/maplibre__maplibre-gl-js/` |
| RSRC-070 | P2 | D11 | Leaflet | Lightweight map alternative | leafletjs.com | `leafletjs.com` | BSD-2-Clause | ~40 KB | Yes | AUTO-GIT / npm | `repositories/` |
| RSRC-071 | P2 | D11 | deck.gl | WebGL2-powered geospatial layers | github.com | `github.com/visgl/deck.gl` | MIT | ~1 MB | Yes | AUTO-GIT / npm | `repositories/` |
| RSRC-072 | P2 | D11 | Cytoscape.js | Graph/network visualization | js.cytoscape.org | `js.cytoscape.org` | MIT | ~200 KB | Yes | AUTO-GIT / npm | `repositories/cytoscape__cytoscape.js/` |
| RSRC-073 | P2 | D11 | Apache ECharts | Charting library | echarts.apache.org | `echarts.apache.org` | Apache-2.0 | ~1 MB | Yes | AUTO-GIT / npm | `repositories/` |
| RSRC-074 | P2 | D11 | React + Next.js | Frontend framework | react.dev | `react.dev` | MIT | Base ~100 KB | Yes | npm | Via package.json |
| RSRC-075 | P2 | D11 | TypeScript | Type-safe JavaScript | typescriptlang.org | `typescriptlang.org` | Apache-2.0 | Dev only | Yes | npm | Via package.json |
| RSRC-076 | P2 | D11 | Apache ECharts timeline component | Temporal visualization | echarts.apache.org | `echarts.apache.org` | Apache-2.0 | Bundled | Yes | npm | — |

**Catalyst deployment implication:** All frontend libraries bundled and deployed via Catalyst Slate / Web Client Hosting. Bundle size must be optimized for Catalyst's hosting limits. Offline/low-bandwidth support should use tile caching and service workers.

### D12 — Backend, Data Engineering, AI, and Platform Resources

| RSRC | Pri | Cat | Resource | Why | Source | URL | License | Auto | Method | Path |
|------|-----|-----|----------|-----|--------|-----|---------|------|--------|------|
| RSRC-077 | P1 | D12 | Python 3.10+ | Primary backend language | python.org | `python.org` | PSF | Yes | AUTO-DIRECT-DOWNLOAD | System install |
| RSRC-078 | P1 | D12 | FastAPI | REST API framework (local dev only) | fastapi.tiangolo.com | `fastapi.tiangolo.com` | MIT | Yes | pip | Via requirements.txt |
| RSRC-079 | P2 | D12 | Shapely + GeoPandas | Geospatial Python processing | shapely.readthedocs.io | `shapely.readthedocs.io` | BSD | Yes | pip | — |
| RSRC-080 | P2 | D12 | Pandas + NumPy | Data manipulation | pandas.pydata.org | `pandas.pydata.org` | BSD | Yes | pip | — |
| RSRC-081 | P2 | D12 | Scikit-learn | ML models | scikit-learn.org | `scikit-learn.org` | BSD | Yes | pip | — |
| RSRC-082 | P2 | D12 | Sentence-Transformers | Embedding models | sbert.net | `sbert.net` | Apache-2.0 | Yes | pip | — |
| RSRC-083 | P2 | D12 | MLflow | ML lifecycle tracking (local dev) | mlflow.org | `mlflow.org` | Apache-2.0 | Yes | pip | — |
| RSRC-084 | P1 | D12 | Node.js 18+ | Catalyst Functions runtime | nodejs.org | `nodejs.org` | MIT | Yes | AUTO-DIRECT-DOWNLOAD | System install |

**Catalyst compatibility note:** FastAPI, MLflow, and other non-Catalyst server frameworks are for local development only. Production on Catalyst uses Functions (Node.js/Python). Locally developed logic is ported to the Functions paradigm.

### D13 — Synthetic Data Resources

| RSRC | Pri | Cat | Resource | Why | Feature | Source | URL | License | Auto | Method | Validate | Path |
|------|-----|-----|----------|-----|---------|--------|-----|---------|------|--------|----------|------|
| RSRC-085 | P1 | D13 | Faker Python library | Core synthetic data generation | All synthetic data | pypi.org | `pypi.org/project/Faker/` | MIT | Yes | pip install | Test en_IN locale generates valid names/addresses | Via requirements.txt |
| RSRC-086 | P2 | D13 | indic-faker | Kannada-script synthetic text | Kannada UI testing | pypi.org | `pypi.org/project/indic-faker/` | MIT | Yes | pip install | Kannada locale generates native-script text | Via requirements.txt |
| RSRC-087 | P1 | D13 | Synthetic data generation scripts | Custom FIR/entity generation | All prototype data | Project code | `scripts/data/generate_synthetic.py` | MIT (project) | Semi | Write | Validates against ERD schema | `scripts/data/` |

**Synthetic data plan:**

| Aspect | Specification |
|--------|---------------|
| Scale tiers | 200 records (smoke test), 2,000 records (demo), 10,000 records (stress test) |
| Entity types | FIR/Case, Person (complainant, accused, witness, victim), Vehicle, Evidence, Relationship |
| Referential integrity | Every foreign key resolves; no orphan records |
| Realistic distributions | District distribution approximates KSP crime review proportions |
| Seed control | Deterministic seed per tier for reproducibility |
| Scenario labels | Planted patterns: hotspot cluster, serial MO, linked cases, anomaly spike |
| Ground-truth links | Every synthetic record's "known truth" tracked in companion metadata |
| Bias controls | Balanced across synthetic demographic categories; documented distributions |
| Privacy tests | No record matches any real person (automated check + manual spot check) |
| Marking | Every file and every record contains `SYNTHETIC` in its metadata; header comment in every file |
| Synthetic data cards | One card per synthetic dataset describing generation method, distributions, and limitations |

### D14 — Security, Privacy, Governance, and Compliance Resources

| RSRC | Pri | Cat | Resource | Why | Source | URL | License | Auto | Method | Path |
|------|-----|-----|----------|-----|--------|-----|---------|------|--------|------|
| RSRC-088 | P4 | D14 | OWASP ASVS (Application Security Verification Standard) | Security baseline reference | owasp.org | `owasp.org` | CC-BY-SA | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/security/` |
| RSRC-089 | P4 | D14 | OWASP API Security Top 10 | API security reference | owasp.org | `owasp.org` | CC-BY-SA | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/security/` |
| RSRC-090 | P4 | D14 | NIST Cybersecurity Framework (CSF) | Security governance reference | nist.gov | `nist.gov` | US public domain | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/security/` |
| RSRC-091 | P4 | D14 | NIST AI Risk Management Framework (AI RMF) | AI governance reference | nist.gov | `nist.gov` | US public domain | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/security/` |
| RSRC-092 | P4 | D14 | OWASP Dependency-Check | SCA tool reference | owasp.org | `owasp.org` | Apache-2.0 | Yes | AUTO-DIRECT-DOWNLOAD | `resources/standards/security/` |

---

## E. Feature-to-Data Matrix

| Feature | Required input data | Optional enrichment | Min prototype fields | Enterprise fields | Preprocessing | Model/analytics | Output | Explainability | Ground truth | Eval method | Risk | Human approval | Catalyst service |
|---------|-------------------|-------------------|--------------------|-----------------|--------------|-----------------|--------|---------------|-------------|------------|------|---------------|-----------------|
| Crime-trend dashboards | CaseMaster.date, CrimeHead | NCRB/KS baselines | crime_type, date, district | Multiple subcategory drill-down | Date parsing, district code join | Aggregation/grouping | Time-series chart | N/A (descriptive) | None | Schema checks | Low | None | Data Store + QuickML |
| District/station drill-down | CaseMaster.district, police_station | Boundary files | district, station | Taluk, beat, jurisdiction | Admin code normalization | Hierarchical agg | Drill-down dashboard | N/A | None | Data coverage check | Low | None | Data Store |
| Spatiotemporal hotspots | Inv_OccuranceTime lat/long, crime_type | OSM POIs, Bhuvan LULC | lat, long, crime_type | Time-weighted density | Coordinate validation, CRS normalization | H3 hexbin / KDE | Heat map layer | Visual density | Manufactured synthetic hotspot | Precision-recall on planted clusters | Medium | SCRB review before operational use | QuickML |
| Emerging-spike alerts | Rolling crime counts | Weather, holidays | district, crime_type, week | Multi-factor adjusted | Rolling window | Z-score / STL decomposition | Alert with magnitude | Deviation components shown | Historical baseline | Precision-recall | Medium | Officer reviews before resource reallocation | Functions + Cron |
| MO similarity | BriefFacts, CrimeHead text | R026 entity patterns | Free text, method fields | Structured MO taxonomy | Text embedding | Cosine similarity on BERT embeddings | Matched cases with score | Matched text highlighted | Labeled MO examples (synthetic) | Hit rate at k | Medium | Investigator confirms match | QuickML |
| Repeat-pattern analysis | AccusedDetails, CrimeHead | VehicleLink | Person ID, crime_type, date | Geo-temporal sequence | Entity resolution dedup | Sequence pattern mining | Pattern report | Pattern visualization | Planted repeat patterns (synthetic) | Precision-recall | Medium | Officer reviews findings | Functions |
| Cross-case linking / entity resolution | Accused, Victim, Complainant | FollowTheMoney patterns | name, age, address | Multiple ID types | Blocking + weighted similarity | Python record linkage | Match candidates with score | Match confidence components shown | Planted duplicate person test | F1 on planted duplicates | High | Investigator confirms merge | Functions |
| POLE graph | All resolved entities + relationships | OSM, VehicleLink | Entity ID, relationship type | Full POLE with temporal edges | Entity resolution, relationship extraction | NetworkX graph traversal | Interactive graph visualization | Path shown, not score | Planted graph communities | Path completeness | Medium | Read-only for investigators | Data Store + Functions |
| Entity resolution | Name, age, address across tables | Multiple ID sources | Name, DOB, address | Biometric, ID references | Blocking, normalization | Weighted similarity | Match pairs with confidence | Feature-level match breakdown | Planted duplicates | F1, false positive rate | High | Human-in-loop before merge | Functions |
| Network community detection | Entity resolution output, relationship edges | OSM social infrastructure | Entity graph | Full POLE graph | Graph construction | Community detection (Louvain/Leiden) | Community clusters | Cluster membership shown | Planted graph communities | Modularity, NMI | Medium | Analyst review | Functions + QuickML |
| Anomaly detection | All crime features | Temporal, weather context | Multiple feature dimensions | Learned normal patterns | Feature engineering | Isolation Forest / autoencoder | Anomaly list with score | Feature contribution to anomaly score | Planted anomalies | Precision, recall, F1 | Medium | Officer reviews flagged items | QuickML |
| Workload dashboard | CaseMaster.assigned_officer, station | Employee table | Officer, station, case count | Case complexity, clearance time | Aggregation | Descriptive stats | Load visualization | N/A | None | Data accuracy | Low | Command-staff review | Data Store |
| Patrol resource recommendation | Workload, hotspot, temporal | Traffic, weather | District, time, crime count | Real-time officer location | Feature engineering | Optimization model (Vision) | Resource suggestion | Constraints shown | Historical effectiveness | Precision-recall | Medium | Command authorization | QuickML (Vision) |
| Natural-language query (RAG) | Case summaries, crime data | BNS/legal text | Curated case text | Full case corpus | Text chunking, embedding | RAG over QuickML LLM | Answer with citations | Cited source per answer | Rehearsed Q&A set | Faithfulness, citation accuracy | Medium (hallucination) | Flag unverified answers | QuickML |
| Evidence-backed report generation | Case, evidence, chargesheet | BNS legal text | Case outcome, evidence refs | Full evidence chain | Template selection | Template + RAG-grounded drafting | PDF report | Every claim traces to source | Sample report review | Completeness, accuracy | Medium | Human reviews before release | SmartBrowz + QuickML |
| Data-quality monitoring | All ingested tables | — | Schema, nulls, duplicates | Full DQ framework | Schema validation | Rule-based checks | DQ dashboard | Rule-based (fully explainable) | None | DQ metrics | Low | None (internal ops) | Functions + Cron |
| Model monitoring | Model predictions, actual outcomes | — | Prediction, actual, timestamp | Full drift + performance | Feature alignment | Drift detection, performance tracking | Monitor dashboard | Performance metrics | Ground truth labels | Drift metrics, accuracy | Medium | Model governance board | Functions |
| Governance/audit dashboard | AuditLog | Access patterns | Actor, action, timestamp | Full compliance trail | Log parsing | Rule-based compliance check | Audit report | Fully explainable by design | None | Completeness | Low (by design — IS the safeguard) | Compliance-reporting role | Data Store + API Gateway RBAC |

---

## F. Automated vs. Manual Acquisition Matrix

| Code | Meaning | Example resources | Why |
|------|---------|-------------------|-----|
| AUTO-API | Public API, no login, rate-limited | RSRC-030 (OSM Overpass), RSRC-039 (Open-Meteo) | Published, rate-limited, no auth needed for reasonable use |
| AUTO-DIRECT-DOWNLOAD | Public file/page fetch | RSRC-025 (NCRB PDF), RSRC-043 (BNS text) | Static public content; direct URL available |
| AUTO-GIT | Clone with pinned commit | RSRC-055 (OpenAleph), RSRC-056 (Kepler.gl) | Open-source repos; commit-pinned for reproducibility |
| AUTO-BROWSER-WITH-USER-SESSION | Requires your login | RSRC-001 (Hack2Skill dashboard) | Behind authentication; not scriptable unattended |
| SEMI-AUTOMATED | Scriptable once human confirms method | RSRC-033 (police boundaries), RSRC-040 (IMD data) | Access mechanism not fully confirmed |
| MANUAL-AUTHORIZED | Human does this step directly | RSRC-002 (ERD already in hand), RSRC-032 (Survey of India) | Already provided, or licensing/authority unclear |
| FUTURE-RESTRICTED | Not acquired now; interface contracts only | RSRC-060 (CCTNS) | Requires lawful process (warrant/MOU), not an engineering decision |
| DO-NOT-ACQUIRE | Explicitly excluded | Any caste-linked dataset | Either not a data source or an active bias/legal risk |

---

## G. Download and Storage Architecture

```text
berunda/
├── docs/                          # Enterprise documentation (81+ files)
├── data/
│   ├── organizer/                 # Hack2Skill-provided material (RSRC-001-008)
│   ├── raw/                       # Original downloads, untouched
│   │   ├── ncrb/                  # NCRB crime statistics (RSRC-025-026)
│   │   ├── ksp/                   # Karnataka Police publications (RSRC-027-028)
│   │   ├── ndap/                  # NITI Aayog NDAP data (RSRC-029, RSRC-037)
│   │   ├── census/                # Census of India (RSRC-036)
│   │   └── ...
│   ├── external/                  # API responses, cached (RSRC-030, RSRC-039, RSRC-041)
│   │   ├── osm/                   # OpenStreetMap extracts
│   │   └── weather/               # Open-Meteo / IMD data
│   ├── interim/                   # Partially processed data
│   ├── processed/                 # Feature tables, ready for analytics
│   ├── synthetic/                 # Generated data, always SYNTHETIC_ prefixed
│   ├── samples/                   # Small sample extracts for dev/test
│   └── restricted-placeholders/   # Mock adapters for FUTURE-RESTRICTED items
├── boundaries/                    # Geospatial boundary files
│   ├── karnataka/                 # Admin boundaries (districts, taluks)
│   ├── bhuvan/                    # Bhuvan WMS/WFS layers
│   └── dem/                       # Digital elevation models
├── resources/
│   ├── source-pages/              # Downloaded documentation pages
│   ├── standards/                 # Standards documents
│   │   ├── legal/                 # BNS, BNSS, BSA, DPDP
│   │   ├── security/              # OWASP, NIST
│   │   └── geospatial/            # GeoJSON, OGC
│   ├── papers/                    # Research papers
│   └── licenses/                  # Software licenses
├── repositories/                  # Cloned Git repos, commit-pinned
│   ├── alephdata__aleph/
│   ├── cytoscape__cytoscape.js/
│   ├── maplibre__maplibre-gl-js/
│   └── ...
├── models/                        # Trained/saved models
├── manifests/                     # Acquisition manifests
├── scripts/
│   ├── acquisition/               # Download scripts
│   ├── validation/                # Validation scripts
│   └── transformation/            # ETL/transformation scripts
├── reports/                       # Acquisition & validation reports
├── logs/                          # Acquisition action logs
├── quarantine/                    # Fresh downloads, before validation
├── .gitignore
├── .env.example
└── AGENTS.md
```

**Naming rules:**
- Every file under `data/raw/` keeps its original filename plus `_<YYYYMMDD>` acquisition-date suffix
- Every file gets a companion `.sha256` checksum file at acquisition time
- Synthetic files prefixed with `SYNTHETIC_` at the filename level plus `SYNTHETIC` in file metadata
- Repositories stored as `repositories/<owner>__<repo>/`

**Version control rules:**
- `data/raw/`, `data/external/`, `data/synthetic/`, `boundaries/`, and `models/` are Git-ignored
- Use Git LFS for files > 5 MB that must be versioned
- Use DVC for pipeline-tracked data if reproducibility across machines is needed
- Public GitHub remote contains only code, small samples, schemas, and documentation

---

## H. Resource Manifest Specification

### H1. Source Manifest (`manifests/resource_manifest.csv`)

```csv
rsrc_id,priority,category,name,source_url,verified_url,publisher,license,legal_class,expected_format,expected_size_bytes,update_frequency,auto_acquisition,method,date_acquired,checksum_sha256,local_path,status,notes
RSRC-001,P0,D1,Challenge rules,https://hack2skill.com/...,,Hack2Skill,Organizer terms,Authorized,HTML/PDF,,Static,No,AUTO-BROWSER-WITH-USER-SESSION,,,,MISSING,Login-gated
RSRC-025,P0,D3,NCRB Crime in India 2022,https://ncrb.gov.in/...,https://ncrb.gov.in,NCRB,Govt publication,Public,PDF,52428800,Annual,Yes,AUTO-DIRECT-DOWNLOAD,2026-07-18,abc123...,data/raw/ncrb/cii_2022.pdf,VERIFIED,
```

### H2. Provenance Record (`manifests/provenance.jsonl`)

```json
{"rsrc_id": "RSRC-039", "source_url": "https://archive-api.open-meteo.com/v1/archive", "access_date": "2026-07-18", "checksum_sha256": "abc123...", "transform_applied": "timezone_normalize_IST", "derived_from": null}
{"rsrc_id": "RSRC-085", "source_url": "https://pypi.org/project/Faker/", "access_date": "2026-07-18", "checksum_sha256": "def456...", "transform_applied": null, "derived_from": null}
```

### H3. License Inventory (`manifests/license_inventory.csv`)

```csv
rsrc_id,resource_name,license_name,license_url,attribution_required,attribution_text,notes
RSRC-030,OpenStreetMap Karnataka POIs,ODbL,https://opendatacommons.org/licenses/odbl/,Yes,"© OpenStreetMap contributors","Required for any published map"
RSRC-069,MapLibre GL JS,BSD-3-Clause,https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt,Yes,"Copyright (c) 2023, MapLibre contributors","BSD-3-Clause with specific attribution text"
```

### H4. Download Manifest (`manifests/download_manifest.csv`)

```csv
rsrc_id,attempted_date,http_status,bytes_received,redirect_chain,error_message,retry_count,success
RSRC-039,2026-07-18T10:00:00Z,200,245000,https://archive-api.open-meteo.com/...,,0,TRUE
RSRC-025,2026-07-18T10:05:00Z,404,0,,File not found at expected URL,1,FALSE
```

### H5. Failure Log (`manifests/failure_log.csv`)

```csv
rsrc_id,attempted_date,failure_reason,next_action,notified
RSRC-025,2026-07-18,URL returned 404,Search data.gov.in for current CCTNS catalog link,TRUE
```

### H6. Approval Register (`manifests/approval_register.csv`)

```csv
rsrc_id,approval_type,reason,approved_by,approval_date,expiry_date
RSRC-001,AUTHENTICATED-SESSION,Dashboard login required to access challenge rules,User Name,2026-07-18,2026-07-28
RSRC-030,LARGE-DOWNLOAD,OSM Karnataka extract may exceed 200 MB,User Name,2026-07-18,
```

### H7. Missing Resource Register (`manifests/missing_resource_register.csv`)

```csv
rsrc_id,impact,priority,acquisition_path,automation_feasibility,deadline,fallback
RSRC-032,No authoritative district boundaries for map layers,HIGH,Survey of India website,MANUAL-AUTHORIZED,Day 5,Use OSM admin boundaries as fallback
```

---

## I. Quality Gates

A resource does not leave `quarantine/` until it passes every applicable gate:

| Gate | What it checks | Applies to | Tools/method |
|------|---------------|-----------|-------------|
| 1. Authenticity | Source matches the verified URL, not a mirror | All | Compare domain, verify redirect chain |
| 2. File integrity | Checksum matches; archive extracts cleanly | All | certutil/shasum, unzip/tar test |
| 3. MIME-type verification | Expected format confirmed | All | file/magic bytes check |
| 4. Schema validity | Required columns present, types as expected | CSV/JSON/Parquet | Pandas schema validation |
| 5. Geometry validity | Valid geometry, coordinates inside Karnataka bbox, CRS = WGS84 | Spatial | Shapely .is_valid, bbox check |
| 6. Temporal validity | Dates parse; no impossible future dates | Temporal | Pandas datetime parse, range check |
| 7. Duplicate detection | No exact-duplicate rows | Tabular | Pandas .duplicated() |
| 8. Missing-value profile | Recorded, not silently dropped | Tabular | Pandas .isnull() summary |
| 9. Admin-code matching | District/station codes join reference set | Karnataka-specific | Cross-reference join |
| 10. Licensing | License on file in license_inventory.csv | All | Manual review of license field |
| 11. Attribution | Attribution recorded if license requires | All | License inventory check |
| 12. Secrets scan | No keys, tokens, or credentials | Code/repos | TruffleHog or equivalent |
| 13. PII scan | No real names/phones/IDs in aggregate/synthetic data | Tabular | Regex patterns, manual spot check |
| 14. Malware scan | Clean for executable/macro formats | EXE/DOCM/XLSM | Defender/ClamAV |
| 15. Synthetic-data marker | SYNTHETIC marker in metadata + filename | Synthetic | Automated check, manual verification |

---

## J. Resource Roadmap

| Phase | Timeline | Focus | Key RSRCs |
|-------|----------|-------|-----------|
| **First 24 hours** | Day 0-1 | Organizer material, Catalyst docs, legal references | RSRC-001-008 (organizer), RSRC-009-024 (Catalyst), RSRC-043-046 (legal) |
| **First 3 days** | Day 1-3 | Enrichment data, synthetic tooling | RSRC-030 (OSM), RSRC-039 (weather), RSRC-085-086 (Faker), RSRC-087 (synthetic scripts) |
| **First week** | Day 4-7 | Baselines, reference repos | RSRC-025-029 (crime stats), RSRC-036-037 (Census/NDAP), RSRC-055-059 (repos) |
| **Prototype freeze** | Day 9-10 | Stop acquiring; validate and polish | All acquired resources |
| **Submission week** | Day 10-11 | Confirm submission format, rehearse demo | RSRC-001, RSRC-005 |
| **Post-hackathon** | After event | Enterprise roadmap items | RSRC-032 (Survey of India), RSRC-033 (police boundaries), RSRC-040 (IMD), RSRC-060 (CCTNS) |

**What NOT to download:**
- RSRC-060 (CCTNS) — no lawful path in an 11-day window
- RSRC-038 (RBI DBIE) — P4, not needed for Phase 1
- RSRC-048 (BPRD handbook) — P4, informative only
- Any caste-linked dataset — DO-NOT-ACQUIRE

---

## K. Final Checklists

### P0 Completion Checklist
- [ ] RSRC-001: Rules/timeline/submission format confirmed
- [ ] RSRC-002: ERD reconciled against uploaded PDF
- [ ] RSRC-003: Data dictionary parsed (if provided)
- [ ] RSRC-005: Judging rubric reviewed
- [ ] RSRC-006: Catalyst credits redeemed and visible
- [ ] RSRC-025: NCRB baseline crime statistics retrieved
- [ ] RSRC-043: BNS/BNSS/BSA legal texts retrieved

### Prototype Readiness Checklist
- [ ] Synthetic dataset generated (RSRC-085, RSRC-087) with planted patterns
- [ ] OSM/Bhuvan enrichment wired into hotspot map
- [ ] Every acquired file has checksum + manifest row
- [ ] Feature-to-data matrix confirmed complete for MVP features
- [ ] Catalyst services (RSRC-009-024) quickstarted and tested

### Legal and Ethical Checklist
- [ ] No caste-linked dataset anywhere in `data/`
- [ ] Caste/religion fields excluded from all model training features
- [ ] BNS/BNSS/BSA references used only as classification reference
- [ ] All synthetic data marked with clear `SYNTHETIC` label
- [ ] No predictive criminality scoring of individuals
- [ ] Human-in-loop points documented for every automated insight

### Catalyst Readiness Checklist
- [ ] Every mandatory service has its doc bookmarked
- [ ] Quickstart run for: Functions, Data Store, API Gateway, Slate, Signals
- [ ] Catalyst CLI installed and authenticated
- [ ] Dev/staging/prod environments configured
- [ ] Secrets managed via Catalyst Connections, not code

### Open-Source Release Checklist
- [ ] Every third-party repo has license recorded in `license_inventory.csv`
- [ ] No incompatible-license code copied wholesale
- [ ] `.gitignore` configured to exclude data, models, secrets
- [ ] README includes license and attribution section
- [ ] SBOM generated for all dependencies

### Demo Evidence Checklist
- [ ] `reports/VALIDATION_REPORT.md` shows every feature's data passed quality gates
- [ ] Rehearsed RAG questions tested against frozen dataset
- [ ] Synthetic planted patterns demonstrable (hotspot, MO similarity, linked cases)
- [ ] Explainability outputs generated for at least one AI feature
- [ ] Audit log shows governance dashboard in action

### Post-Hackathon Backlog
- [ ] Survey of India boundaries (RSRC-032) — licensing confirmation
- [ ] Police jurisdiction boundaries (RSRC-033) — access method confirmation
- [ ] IMD official weather (RSRC-040) — bulk access method
- [ ] CCTNS future integration contract (RSRC-060)
- [ ] Full research literature review (RSRC-062-068)
- [ ] Enterprise portability assessment from Catalyst to open stack
