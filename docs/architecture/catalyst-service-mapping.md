# Catalyst Service Mapping

[//]: # (Document ID: BERUNDA-CATMAP-001 | Version: 1.1 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, DevOps | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-24 | Review: Monthly)

---

## Mandatory Catalyst Service Mapping

| # | Capability | Catalyst Service | Berunda Module | Rationale | MVP Status | Falls Back To |
|---|-----------|-----------------|----------------|-----------|------------|---------------|
| 1 | Serverless functions | Catalyst Functions | All business logic (ingestion, NER, entity resolution, anomaly, fairness) | Stateless, auto-scaling, pay-per-invocation | ✅ MVP | — |
| 2 | Docker image deployment | AppSail (custom OCI) | Kannada NER custom container (STRETCH) | Needed if Phase 2 requires custom model runtime | 🧩 STRETCH | QuickML |
| 3 | Full web app runtime | AppSail (managed) | Graph engine (NetworkX), scikit-learn inference | Persistent Python runtime for graph algorithms | ✅ MVP | Functions |
| 4 | Frontend hosting | Slate / Web Client Hosting | Dashboard SPA | Mandatory frontend host; CDN-backed | ✅ MVP | — |
| 5 | Custom domain + SSL | Domain Mappings | Public-facing portal | Custom URL with TLS | ✅ MVP | — |
| 6 | Relational database | Data Store | Core schema (CaseMaster, Accused, Victim, + Berunda extensions) | Relational integrity for crime data | ✅ MVP | — |
| 7 | Unstructured data | NoSQL | Raw FIR text, BriefFacts full text | Schema flexibility for free-text | ✅ MVP | Data Store |
| 8 | Object storage | Stratus | Evidence files, scanned FIRs | S3-compatible file store | ✅ MVP | — |
| 9 | Cache | Cache | Jurisdiction lookups, aggregated hotspot layers | Reduces repeated Data Store queries | ✅ MVP | Data Store |
| 10 | Full-text search | Data Store (native) | FIR narrative search | Native capability, no extra service needed | ✅ MVP | — |
| 11 | LLM / RAG | QuickML (LLM Serving, RAG) | "Ask Berunda" NL assistant | Native Qwen serving + RAG; no custom hosting | ✅ MVP | Template query bar |
| 12 | ML pipelines (no-code) | QuickML | Risk scoring pipeline setup | Avoids hand-rolling ML infra | ✅ MVP | — |
| 13 | AutoML (tabular) | Zia AutoML / QuickML | Repeat-offender risk model | Native AutoML with feature importance | ✅ MVP | — |
| 14 | OCR / Vision | Zia Services | Scanned FIR OCR (STRETCH) | Needed for scanned document ingestion | 🧩 STRETCH | Manual entry |
| 15 | Voice / speech | Zia Services | Voice FIR intake (VISION) | Deferred to Phase 2+ | 🔭 VISION | — |
| 16 | PDF generation | SmartBrowz | Auto-generated reports (STRETCH) | Headless browser PDF rendering | 🧩 STRETCH | Manual export |
| 17 | User authentication | Authentication | Login, MFA, session management | Built-in auth with MFA support | ✅ MVP | — |
| 18 | API routing / throttling | API Gateway | Front door for all Functions | Auth enforcement + rate limiting | ✅ MVP | — |
| 19 | OAuth tokens | Connections | Future CCTNS API bridge | Needed for real CCTNS integration | 🔭 VISION | — |
| 20 | Scheduled jobs | Cron / Job Scheduling | Anomaly baseline recompute, drift check | Nightly batch operations | ✅ MVP | — |
| 21 | Event functions | Signals + Event Functions | Real-time alert pipeline (VISION) | Deferred to Phase 3 | 🔭 VISION | — |
| 22 | Cross-app event bus | Signals | Multi-district routing (VISION) | Deferred to Phase 3 | 🔭 VISION | — |
| 23 | Workflow orchestration | Circuits | Multi-agent orchestration (VISION) | Deferred to Phase 3+ | 🔭 VISION | — |
| 24 | Transactional email | Mail | Alert notifications to SHOs/SCRB | Spike alerts | ✅ MVP | — |
| 25 | Push notifications | Push Notifications | Mobile hotspot alerts (STRETCH) | Deferred to Phase 2 | 🧩 STRETCH | Email |
| 26 | CI/CD | Pipelines | Build, test, deploy automation | Automated deployment pipeline | ✅ MVP | Manual deploy |

## MVP Service Count: 18 services

The following 18 Catalyst services are used in the MVP:
1. Functions, 2. AppSail, 3. Slate, 4. Domain Mappings, 5. Data Store, 6. NoSQL, 7. Stratus, 8. Cache, 9. QuickML (LLM/RAG), 10. QuickML (pipelines), 11. Zia AutoML, 12. Authentication, 13. API Gateway, 14. Cron, 15. Mail, 16. Pipelines, 17. Full-text search (Data Store native), 18. SmartBrowz (if STRETCH)

## Service Limit Awareness

Each Catalyst service has platform-imposed limits (concurrent executions, storage, API calls per day, etc.). These limits must be reviewed against the demo dataset volume before deployment.

**⚠️ UNVERIFIED — CHECK CATALYST DOCS for current service limits before committing to architecture.**
