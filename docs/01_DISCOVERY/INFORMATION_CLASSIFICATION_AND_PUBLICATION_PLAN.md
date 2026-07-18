# Information Classification and Publication Plan

[//]: # (Document ID: BERUNDA-CLASS-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Team | Source: Source files 1-12 (h2s.zip) | Last Verified: 2026-07-17 | Review: Monthly)

---

## Classification Levels Applied to Documentation Set

| Level | Access Restriction | Examples | Suitable for Public Repo? |
|-------|-------------------|----------|---------------------------|
| PUBLIC | No restriction | README, Glossary, Market analysis, Executive summary | ✅ Yes |
| INTERNAL | Team + organizers | PRD, SRS, Architecture, Data model, API specs, Test strategy | ✅ Yes (with caution) |
| CONFIDENTIAL | Team only | Source ERD reconciliation with specific field mappings, detailed schema | ⚠️ Review before publishing |
| RESTRICTED | Named individuals | Security controls detail, threat model specifics, incident playbook | ❌ No — keep private |

## Document Classification Matrix

| Document | Classification | Rationale |
|----------|---------------|-----------|
| README.md | PUBLIC | Project identity, no sensitive details |
| 00_DOCUMENT_CONTROL.md | PUBLIC | Administrative metadata |
| 00_GLOSSARY.md | PUBLIC | Terminology reference |
| 00_START_HERE.md | PUBLIC | Navigation guide |
| 01_DISCOVERY/SOURCE_INVENTORY_AND_AUTHORITY.md | INTERNAL | Source references, no sensitive data |
| 01_DISCOVERY/CONTRADICTION_ASSUMPTION_AND_GAP_REGISTER.md | INTERNAL | Gap analysis, technical discussion |
| 01_DISCOVERY/EXTERNAL_CLAIM_VERIFICATION_REGISTER.md | INTERNAL | Unverified claims about external systems |
| 01_DISCOVERY/INFORMATION_CLASSIFICATION_AND_PUBLICATION_PLAN.md | INTERNAL | This document |
| 02_STRATEGY_AND_PRODUCT/PROJECT_CHARTER.md | PUBLIC | Mission, vision, objectives |
| 02_STRATEGY_AND_PRODUCT/EXECUTIVE_SUMMARY.md | PUBLIC | Concise overview |
| 02_STRATEGY_AND_PRODUCT/PROBLEM_STAKEHOLDERS_AND_PERSONAS.md | PUBLIC | Stakeholder analysis |
| 02_STRATEGY_AND_PRODUCT/PRODUCT_REQUIREMENTS_DOCUMENT.md | INTERNAL | Detailed product spec |
| 02_STRATEGY_AND_PRODUCT/USE_CASE_CATALOG.md | PUBLIC | Use case descriptions |
| 02_STRATEGY_AND_PRODUCT/MVP_SCOPE_AND_RELEASE_PLAN.md | INTERNAL | Scope decisions, prioritization |
| 02_STRATEGY_AND_PRODUCT/SUCCESS_METRICS_AND_BENEFITS_REALIZATION.md | PUBLIC | Success criteria |
| 03_REQUIREMENTS/SOFTWARE_REQUIREMENTS_SPECIFICATION.md | INTERNAL | Detailed requirements |
| 03_REQUIREMENTS/NON_FUNCTIONAL_REQUIREMENTS.md | INTERNAL | NFRs with security implications |
| 03_REQUIREMENTS/REQUIREMENTS_TRACEABILITY_MATRIX.md | INTERNAL | Cross-reference data |
| 03_REQUIREMENTS/ACCEPTANCE_CRITERIA_AND_DEFINITION_OF_DONE.md | INTERNAL | Quality gates |
| 04_ARCHITECTURE/SYSTEM_CONTEXT_AND_CONTAINER_ARCHITECTURE.md | PUBLIC | High-level diagrams (no sensitive detail) |
| 04_ARCHITECTURE/HIGH_LEVEL_DESIGN.md | INTERNAL | Module design |
| 04_ARCHITECTURE/LOW_LEVEL_DESIGN.md | CONFIDENTIAL | Component internals, data flow details |
| 04_ARCHITECTURE/CATALYST_SERVICE_MAPPING.md | INTERNAL | Service-to-feature mapping |
| 04_ARCHITECTURE/INTEGRATION_AND_EVENT_ARCHITECTURE.md | INTERNAL | Integration patterns |
| 04_ARCHITECTURE/ADR/*.md | INTERNAL | Design decisions |
| 05_DATA/SOURCE_ERD_RECONCILIATION.md | **CONFIDENTIAL** | Contains organizer schema details |
| 05_DATA/CANONICAL_DATA_MODEL.md | INTERNAL | Unified model (source + extension) |
| 05_DATA/DATA_DICTIONARY.md | **CONFIDENTIAL** | Field-level details from source schema |
| 05_DATA/ENTITY_RESOLUTION_SPECIFICATION.md | INTERNAL | Algorithm specification |
| 05_DATA/SYNTHETIC_DATA_SPECIFICATION.md | PUBLIC | Synthetic data rules, no real data |
| 05_DATA/DATA_ARCHITECTURE.md | INTERNAL | Data flow and storage |
| 05_DATA/DATA_QUALITY_PROFILING_AND_VALIDATION_PLAN.md | INTERNAL | Quality rules |
| 05_DATA/DATA_GOVERNANCE_RETENTION_AND_PROVENANCE.md | INTERNAL | Governance rules |
| 06_AI_AND_ANALYTICS/AI_ML_SYSTEM_SPECIFICATION.md | INTERNAL | Model specs, feature engineering |
| 06_AI_AND_ANALYTICS/RAG_KNOWLEDGE_BASE_AND_GROUNDING_SPEC.md | INTERNAL | RAG implementation |
| 06_AI_AND_ANALYTICS/RESPONSIBLE_AI_AND_HUMAN_OVERSIGHT.md | PUBLIC | Ethics and governance |
| 08_SECURITY_PRIVACY_GOVERNANCE/SECURITY_ARCHITECTURE.md | **RESTRICTED** | Security controls |
| 08_SECURITY_PRIVACY_GOVERNANCE/THREAT_MODEL.md | **RESTRICTED** | Vulnerability analysis |
| 08_SECURITY_PRIVACY_GOVERNANCE/PRIVACY_IMPACT_ASSESSMENT.md | INTERNAL | Privacy analysis |
| 08_SECURITY_PRIVACY_GOVERNANCE/AI_IMPACT_ASSESSMENT.md | INTERNAL | AI risk assessment |
| 08_SECURITY_PRIVACY_GOVERNANCE/ACCESS_CONTROL_MATRIX.md | **RESTRICTED** | Detailed role permissions |
| 08_SECURITY_PRIVACY_GOVERNANCE/AUDIT_LOGGING_AND_EVIDENCE_INTEGRITY.md | INTERNAL | Audit design |
| 08_SECURITY_PRIVACY_GOVERNANCE/INCIDENT_RESPONSE_AND_BREACH_PLAYBOOK.md | **RESTRICTED** | Incident response |
| 11_DELIVERY/IMPLEMENTATION_PLAN.md | INTERNAL | Build timeline |
| 11_DELIVERY/PRIORITIZED_PRODUCT_BACKLOG.md | INTERNAL | Task breakdown |
| 11_DELIVERY/RISK_REGISTER.md | INTERNAL | Risk analysis |
| 11_DELIVERY/HACKATHON_DEMO_AND_PITCH_PLAN.md | INTERNAL | Demo strategy |
| 11_DELIVERY/SUBMISSION_READINESS_CHECKLIST.md | INTERNAL | Pre-submission checks |
| 11_DELIVERY/ENTERPRISE_ROADMAP.md | PUBLIC | Future phases |

## Public Repository Guidelines

Content that may appear in a public GitHub repository:

1. All PUBLIC-classified documents
2. INTERNAL-classified documents only after review — strip specific security/privacy details
3. **Never** any CONFIDENTIAL or RESTRICTED content
4. **Never** real person-level data (synthetic only, clearly labeled)
5. **Never** organizer schema field details from the ERD PDF (use generalized structural descriptions only)

## Confidential Schema Handling

The source ERD PDF is marked "Karnataka Police Department | Confidential." The following rules apply:

- **DO NOT** include the full ERD or verbatim table/column extracts in public files
- **DO NOT** expose `CasteMaster` / `ReligionMaster` lookup values in public docs
- **DO** describe the schema structure in INTERNAL files for development use
- **DO** map fields conceptually (e.g., "the schema has a many-to-many relationship between ArrestSurrender and Accused") without exposing the exact column names from the confidential source
