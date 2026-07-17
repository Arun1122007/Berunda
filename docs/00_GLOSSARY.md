# Glossary

[//]: # (Document ID: BERUNDA-GLOSSARY-001 | Status: DRAFT | Classification: PUBLIC)

---

## Terms and Acronyms

| Term | Definition |
|------|-----------|
| ABAC | Attribute-Based Access Control — authorization based on user/resource attributes (target state, Phase 3+) |
| ADR | Architecture Decision Record — captures a design choice with context, alternatives, and rationale |
| API Gateway | Catalyst service for API routing, throttling, and authentication enforcement |
| AppSail | Catalyst managed runtime for containerized applications (Python/FastAPI) |
| BUILDABLE | Feasibility tag: realistic for 2 people in the hackathon time window |
| Catalyst | Zoho's cloud platform — mandatory deployment target for this datathon |
| CCTNS | Crime and Criminal Tracking Network & Systems — India's national police digitization system |
| Circuits | Catalyst service for multi-step workflow orchestration (target state) |
| CRUD | Create, Read, Update, Delete — standard database operations |
| Data Store | Catalyst's relational database service (MySQL-compatible) |
| DPDP Act | Digital Personal Data Protection Act, 2023 — India's data protection law |
| DPDP Rules 2025 | The operational rules under DPDP Act, notified November 2025 |
| Entity Resolution | Process of identifying when multiple records refer to the same real-world entity (person) |
| FIR | First Information Report — initial report of a cognizable offense to police |
| Faker | Python library for generating synthetic data, supporting `en_IN` locale for Indian names/addresses |
| Functions | Catalyst serverless function service for stateless business logic |
| Gandaberunda | Two-headed mythical bird — Karnataka's state emblem and project namesake |
| Gantt | Timeline visualization (Mermaid format used in roadmap documents) |
| indic-faker | Python library for generating Indian-language synthetic data (8 scripts including Kannada) |
| IO | Investigating Officer — police officer investigating a case |
| IPC | Indian Penal Code (being replaced by BNS 2023) |
| KDE | Kernel Density Estimation — statistical method for hotspot detection |
| LLM | Large Language Model — used for natural-language query and RAG |
| MFA | Multi-Factor Authentication |
| MO | Modus Operandi — characteristic method of operation of an offender |
| Mermaid | Markdown-based diagramming language (flowcharts, ERDs, Gantt charts) |
| MOU | Memorandum of Understanding — required for real CCTNS data access |
| MVP | Minimum Viable Product — the hackathon deliverable |
| NCRB | National Crime Records Bureau — India's central crime statistics agency |
| NER | Named Entity Recognition — extracting persons, locations, organizations from text |
| NoSQL | Catalyst's unstructured data store (for free-text, OSINT captures) |
| OSINT | Open-Source Intelligence — publicly available information gathering |
| QuickML | Catalyst's AI/ML service offering LLM serving, RAG, and AutoML |
| RAG | Retrieval-Augmented Generation — LLM answer grounded in retrieved source documents |
| RBAC | Role-Based Access Control — Phase 1 authorization model |
| SCRB | State Crime Records Bureau — Karnataka's state-level crime records agency |
| SHO | Station House Officer — officer in charge of a police station |
| Signals | Catalyst's event-driven messaging service (target state, Phase 3+) |
| Slate | Catalyst's web client hosting service for frontend SPAs |
| SmartBrowz | Catalyst's PDF/report generation service using headless browser |
| STRETCH | Feasibility tag: doable if Phase 1 progresses ahead of schedule |
| Stratus | Catalyst's object storage service (S3-compatible) for evidence files |
| STRIDE | Microsoft's threat modeling methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) |
| Synthetic Data | Artificially generated data that mimics real data — clearly labeled, no real PII |
| VISION | Feasibility tag: documented for future phases, not built in the hackathon |
| Zia | Catalyst's AI service suite including OCR, image recognition, and AutoML |

## Project-Specific Terms

| Term | Definition |
|------|-----------|
| Berunda Extension Tables | Tables added by Project Berunda beyond the source schema (PersonEntity, RelationshipEdge, RiskScore, AuditLog, etc.) |
| Hidden-Link Discovery | The process of surfacing connections across cases that appear unrelated in isolated records |
| Investigation Assistant | "Ask Berunda" — the RAG-based natural-language query feature |
| PersonEntity | Berunda's deduplicated cross-case identity table, resolving the per-case scoping of source Accused/Victim records |
| Repeat-Offender Risk Score | Explainable risk score based on offense history, recency, and offense-type diversity — never on identity markers |
| Source Schema | The organizer-provided Karnataka Police FIR schema (27+ tables from the ERD PDF) |
