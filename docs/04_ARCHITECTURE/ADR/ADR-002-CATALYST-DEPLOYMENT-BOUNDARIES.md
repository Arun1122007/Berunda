# ADR-002: Catalyst Deployment Boundaries

[//]: # (Document ID: ADR-002 | Status: APPROVED | Classification: INTERNAL)

---

## Context

The datathon requires mandatory deployment on Catalyst by Zoho. Third-party alternatives may affect submission validity. Several source documents suggest Catalyst-native services.

## Decision

All Phase 1 services run entirely within Catalyst:

| Component | Catalyst Service |
|-----------|-----------------|
| Frontend hosting | Slate / Web Client Hosting |
| API gateway | Catalyst API Gateway |
| Business logic | Catalyst Functions |
| Graph compute | Catalyst AppSail (Python) |
| Relational data | Catalyst Data Store |
| Unstructured data | Catalyst NoSQL |
| File storage | Catalyst Stratus |
| Cache | Catalyst Cache |
| AI/LLM | Catalyst QuickML |
| OCR/vision | Catalyst Zia Services |
| Auth | Catalyst Authentication |
| Scheduling | Catalyst Cron |
| Email | Catalyst Mail |
| CI/CD | Catalyst Pipelines |

## Rationale

- Full Catalyst compliance is mandatory for submission validity
- All these services are available in the Catalyst free tier (under credit allocation)
- No external infrastructure (AWS, GCP, Azure, Neo4j Cloud, etc.) is used in Phase 1
- External data sources (OpenStreetMap API, public statistics) are accessed as API clients, not infrastructure dependencies

## Consequences

- Positive: Single-vendor accountability, simplified deployment
- Positive: Full compliance with mandatory-deployment rule
- Positive: Catalyst documentation serves as single source of truth for platform capabilities
- Negative: Cannot use specialized services (Neo4j Aura, Elasticsearch Cloud) that might offer better performance
- Negative: Must work within Catalyst resource limits (UNVERIFIED — needs verification against current Catalyst docs)

## Status

APPROVED
