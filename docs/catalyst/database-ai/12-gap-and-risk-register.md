# 12 Gap and Risk Register

This document tracks identified architectural gaps and operational risks in the Berunda system regarding the Catalyst Data Store and AI implementation.

## 1. Architectural Gaps
| ID | Component | Gap | Remediation Plan |
|---|---|---|---|
| G-01 | Database | Deeply nested `SQLAlchemy` queries in `src/services` are difficult to translate directly to `ZCQL` in the `CatalystAdapter`. | Transition complex analytical aggregations (like hotspot plotting) to Catalyst Event Functions that pre-compute and store the results in Catalyst Cache, allowing the API route to just serve the cached JSON. |
| G-02 | AI RAG | Catalyst Zia currently lacks an off-the-shelf "Vector Store" matching standard `pgvector`. | Utilize Catalyst Stratus for document storage, and rely on QuickML's integrated Knowledge Base abstraction instead of managing custom embeddings. |

## 2. Operational Risks
| ID | Risk | Impact | Mitigation Strategy |
|---|---|---|---|
| R-01 | Free Tier Data Store Row Limit | High | Clean up test data routinely. Avoid storing unstructured audit logs in Data Store; push them to NoSQL or Stratus. |
| R-02 | AppSail Memory constraints (256MB) | High | Offload memory-heavy pandas dataframes to standalone Catalyst serverless functions (which have independent limits) or optimize streaming. |
| R-03 | AI Prompt Injection | Critical | All prompts must pass through the Guardrails service. Log all injections in AuditLog. |
