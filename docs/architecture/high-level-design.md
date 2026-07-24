# High-Level Design

[//]: # (Document ID: BERUNDA-HLD-001 | Version: 1.1 | Status: APPROVED | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Architects | Source: 01_Enterprise_Blueprint + ERD PDF + ADR decisions | Last Verified: 2026-07-23 | Review: Monthly)

---

## 1. Architectural Style

**Phase 1:** Modular Functions + API Gateway — NOT full microservices, NOT event-driven. A limited number of deployable units with explicit module boundaries and contracts. This is the smallest credible architecture for a 2-person team.

**Target State (Phase 3+):** Event-driven mesh with Catalyst Signals event bus, Circuits workflow orchestration, and CQRS read/write separation.

## 2. Module Overview

| Module | Responsibility | Deployable | MVP |
|--------|---------------|-----------|-----|
| FIR Ingestion | Parse, validate, import structured FIR data | Catalyst Function | ✅ |
| NER Extraction | Extract entities from free-text FIR narrative | Catalyst Function | ✅ |
| Entity Resolution | Match persons across cases | Catalyst Function | ✅ |
| Risk Scoring | Compute explainable repeat-offender scores | QuickML AutoML | ✅ |
| Hotspot Analysis | KDE/hexbin aggregation for hotspot detection | Catalyst Function | ✅ |
| Anomaly Detection | Z-score spike detection | Catalyst Function | ✅ |
| Link Analysis | Graph traversal over relationship edges | AppSail (NetworkX) | ✅ |
| RAG Query | Natural-language Q&A over case corpus | QuickML LLM + RAG | ✅ |
| Auth & RBAC | User authentication and role-based access | Catalyst Auth | ✅ |
| Audit Logging | Immutable audit trail | Catalyst Function | ✅ |
| Fairness Check | Verify model exclusion and role restriction | Catalyst Function | ✅ |

## 3. Data Flow: FIR Ingestion

```mermaid
sequenceDiagram
    participant User as Investigator
    participant UI as Dashboard
    participant GW as API Gateway
    participant FN as Ingestion Function
    participant DS as Data Store
    participant NER as NER Function
    participant ER as Entity Resolution
    participant AUD as AuditLog

    User->>UI: Upload FIR Excel/CSV
    UI->>GW: POST /api/v1/fir
    GW->>FN: Route to ingestion function
    FN->>FN: Validate schema & data
    FN->>DS: Insert CaseMaster + linked tables
    FN->>NER: Trigger NER on BriefFacts
    NER->>NER: Extract entities (spaCy)
    NER->>DS: Write to PersonEntityLink, VehicleLink
    NER->>ER: Trigger entity resolution
    ER->>DS: Query existing PersonEntity
    ER->>DS: Create/update PersonEntity + link
    FN->>AUD: Log import event
    FN->>UI: Return success + summary
```

## 4. Data Flow: Entity Resolution

```mermaid
sequenceDiagram
    participant NER as NER Function
    participant ER as Entity Resolution
    participant DS as Data Store
    participant AUD as AuditLog
    participant UI as Dashboard

    NER->>ER: New person name + age + address
    ER->>DS: Query PersonEntity (blocking: district + age band)
    DS->>ER: Candidate entities list
    ER->>ER: Compute weighted similarity for each candidate
    alt Confidence > HIGH_THRESHOLD
        ER->>DS: Auto-link to existing PersonEntity
    else Confidence > LOW_THRESHOLD (grey zone)
        ER->>DS: Create tentative link
        ER->>UI: Flag for manual review
        User->>ER: Confirm or reject match
    else Confidence < LOW_THRESHOLD
        ER->>DS: Create new PersonEntity
    end
    ER->>AUD: Log resolution event
```

## 5. Data Flow: Hotspot/Anomaly Pipeline

```mermaid
sequenceDiagram
    participant CRON as Cron Schedule
    participant FN as Hotspot Function
    participant DS as Data Store
    participant CACHE as Cache
    participant UI as Dashboard

    CRON->>FN: Trigger nightly recompute
    FN->>DS: Query incidents by (district, crime_type, week)
    DS->>FN: Rolling count data
    FN->>FN: Compute hexbin aggregation
    FN->>FN: Compute z-score vs historical baseline
    FN->>DS: Write hotspot layers + anomaly alerts
    DS->>CACHE: Update cached aggregates
    User->>UI: Load hotspot map
    UI->>CACHE: Request hotspot data
    CACHE->>UI: Return cached layers + alerts
```

## 6. Data Flow: RAG Query

```mermaid
sequenceDiagram
    participant User as Investigator
    participant UI as Dashboard
    participant GW as API Gateway
    participant RAG as QuickML RAG
    participant DS as Data Store
    participant AUD as AuditLog

    User->>UI: Type question: "Show me all open cases linked to vehicle KA-05-XXXX"
    UI->>GW: POST /api/v1/rag/query
    GW->>RAG: Route to RAG service
    RAG->>RAG: Retrieve relevant case documents
    RAG->>RAG: Generate grounded answer with citations
    RAG->>DS: Query case details for citation verification
    RAG->>UI: Return answer + citations
    RAG->>AUD: Log query + answer
    UI->>User: Display cited answer
```

## 7. Data Flow: Auth/Audit

```mermaid
sequenceDiagram
    participant User as All Users
    participant UI as Dashboard
    participant AUTH as Catalyst Auth
    participant GW as API Gateway
    participant MOD as Any Module
    participant AUD as AuditLog

    User->>UI: Access dashboard
    UI->>AUTH: Redirect to login
    AUTH->>AUTH: Verify credentials + MFA
    AUTH->>UI: Return session token
    UI->>GW: Request with token
    GW->>GW: Verify token + RBAC permissions
    GW->>MOD: Route authorized request
    MOD->>AUD: Log action (who, what, when, why)
    MOD->>UI: Return response
```
